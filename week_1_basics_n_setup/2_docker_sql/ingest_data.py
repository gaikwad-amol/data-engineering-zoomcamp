import pandas as pd
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name=params.table_name
    csv_name = params.url

    # os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    dataframe_iterator = pd.read_csv(csv_name, iterator= True, chunksize=100000)
    dataframe = next(dataframe_iterator)

    dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
    dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
    dataframe.head(n=0).to_sql(name=table_name, con = engine, if_exists='replace')
    dataframe.to_sql(name=table_name, con = engine, if_exists='append')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write results to')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()

    main(args)