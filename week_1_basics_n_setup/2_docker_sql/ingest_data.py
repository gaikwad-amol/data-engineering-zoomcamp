import pandas as pd
from sqlalchemy import create_engine
import argparse

def main(params):
    database_url=params.database_url
    csv_url = params.csv_url
    table_name = params.table_name

    # os.system(f"wget {url} -O {csv_name}")
    print('creating engine with given database url')
    engine = create_engine(f'{database_url}')
    print('Reading the file at - ' + csv_url)
    dataframe_iterator = pd.read_csv(csv_url, iterator= True, chunksize=100000)
    dataframe = next(dataframe_iterator)
    print('dataframe len is ' + str(len(dataframe)))

    dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
    dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
    print('creating table')
    dataframe.head(n=0).to_sql(name=table_name, con = engine, if_exists='replace')
    print('inserting table')
    dataframe.to_sql(name=table_name, con = engine, if_exists='append')
    print('ingestion complete!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--database_url', help='database url')
    parser.add_argument('--table_name', help='name of the table where we will write results to')
    parser.add_argument('--csv_url', help='url of the csv file')
    args = parser.parse_args()

    main(args)