from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os
import pyarrow.parquet as pq

def main(params):
    database_url=params.database_url
    csv_url = params.csv_url
    table_name = params.table_name

    if csv_url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    print('downloading file ' + csv_url)
    os.system(f"wget {csv_url} -O {csv_name}")
    print('creating engine with given database url')
    engine = create_engine(f'{database_url}')
    # print('Opening the file at - ' + csv_url)
    # parquet_file = pq.ParquetFile(csv_name)
    # first_row_group = parquet_file.read_row_group(0).to_pandas()
    # first_row_group.to_sql(table_name, engine, if_exists='replace')
    # chunk_size = 100
    # for i in range(0, parquet_file.count_rows, chunk_size):
    #     t_start = time()
    #     # Read a chunk of rows
    #     chunk_df = parquet_file.read_row_group(i // chunk_size).to_pandas()
    #     chunk_df.to_sql(table_name, engine, if_exists='append', index=False)
    #     t_end = time()
    #     print('inserted another chunk, took %.3f secs' % (t_start - t_end))

    # #---------------
    dataframe_iterator = pd.read_csv(csv_url, iterator= True, chunksize=1000)
    dataframe = next(dataframe_iterator)
    print('dataframe len is ' + str(len(dataframe)))

    dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
    dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
    print('creating table')
    dataframe.head(n=0).to_sql(name=table_name, con = engine, if_exists='replace')
    print('inserting first chunk')
    dataframe.to_sql(name=table_name, con = engine, if_exists='append')
    print('inserted first chunk')
    while True:
        try:
            t_start = time()
            dataframe = next(dataframe_iterator)
            dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
            dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
            dataframe.to_sql(name=table_name, con = engine, if_exists='append')
            t_end = time()
            print('inserted another chunk, took %.3f secs' % (t_end - t_start))
        except StopIteration:
            print('ingestion complete!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--database_url', help='database url')
    parser.add_argument('--table_name', help='name of the table where we will write results to')
    parser.add_argument('--csv_url', help='url of the csv file')
    args = parser.parse_args()

    main(args)