## Airflow local setup
Refer the page https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2022/week_2_data_ingestion/airflow/1_setup_official.md

Create a Dockerfile to install gcloud cli tool in the airflow
Set the environment variables that are asked.
I faced an error for using user root for pip installation. I have switched to airflow user for requirements.txt installation and back to user root as the GCP thing needs to be done.


Whenever changing the Dockerfile
```
docker-compose build
```
Run the initialisation service
```
UID=$(id -u) GID=$(id -g) docker-compose up airflow-init
```
once success then
```
UID=$(id -u) GID=$(id -g) docker-compose up
```
NOTE: Facing issues with the user permissions. In the docker-compose.yaml for x-airflow-common: changed user from
user: `"${AIRFLOW_UID:-50000}:0"`
to 
user: `"${AIRFLOW_UID}:${AIRFLOW_GID}"`

Also, in airflow-init: changed user from 
`chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}`
to
`chown -R "${UID}:${GID}" /sources/{logs,dags,plugins}`
