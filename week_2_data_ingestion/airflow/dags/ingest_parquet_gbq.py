from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
)

# Environment variables
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "raw_trips_data_all")

# Dataset details
dataset_url = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
)
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# Default DAG arguments
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


# Function to upload file to Google Cloud Storage
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    print(
        f"Uploading {source_file_name} to GCS bucket {bucket_name} as {destination_blob_name}."
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"Uploaded {source_file_name} to {destination_blob_name}.")


# Define DAG
with DAG(
    dag_id="ingest_csv_to_gbq",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["dct"],
) as dag:

    # Task 1: Download dataset via BashOperator
    download_dataset_task = BashOperator(
        task_id="download_parquet",
        bash_command=f"""
        filename=$(basename {dataset_url}) && \
        curl -SSL {dataset_url} -o {path_to_local_home}/$filename && \
        echo $filename
        """,
        do_xcom_push=True,
    )

    # Task 2: Upload file to GCS using PythonOperator
    upload_to_gcs_task = PythonOperator(
        task_id="upload_parquet_to_gcs",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": BUCKET,
            "source_file_name": f"{path_to_local_home}/{{{{ ti.xcom_pull(task_ids='download_parquet') }}}}",
            "destination_blob_name": f"raw/{{{{ ti.xcom_pull(task_ids='download_parquet') }}}}",
        },
    )

    upload_dataset_to_gbq_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/*"],
            },
        },
    )

    # Set task dependencies
    download_dataset_task >> upload_to_gcs_task >> upload_dataset_to_gbq_task
