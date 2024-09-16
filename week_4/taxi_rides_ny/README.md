```
CREATE OR REPLACE EXTERNAL TABLE `learn-from-datatalksclub.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_nyc_taxi_data/GreenTaxiTripRecords_2022/green_tripdata_*.parquet']
);

CREATE OR REPLACE EXTERNAL TABLE `learn-from-datatalksclub.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_nyc_taxi_data/YellowTaxTripRecords_2019/yellow_tripdata_*.parquet']
);

CREATE OR REPLACE EXTERNAL TABLE `learn-from-datatalksclub.nytaxi.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_nyc_taxi_data/fhvTipdataRecords_2019/fhv_tripdata_*.parquet']
);

CREATE OR REPLACE TABLE `learn-from-datatalksclub.nytaxi.green_tripdata` AS
SELECT * FROM `learn-from-datatalksclub.nytaxi.external_green_tripdata`;

CREATE OR REPLACE TABLE `learn-from-datatalksclub.nytaxi.yellow_tripdata` AS
SELECT * FROM `learn-from-datatalksclub.nytaxi.external_yellow_tripdata`;

CREATE OR REPLACE TABLE `learn-from-datatalksclub.nytaxi.fhv_tripdata` AS
SELECT * FROM `learn-from-datatalksclub.nytaxi.external_fhv_tripdata`;

```

```
dbt init
dbt build
```