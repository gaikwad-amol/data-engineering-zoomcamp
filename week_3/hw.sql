--Create an external table using the Green Taxi Trip Records Data for 2022
CREATE OR REPLACE EXTERNAL TABLE `learn-from-datatalksclub.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://green_taxi_trip_records_2022/green_tripdata_*.parquet']
);

-- Check green trip data
SELECT * FROM `learn-from-datatalksclub.nytaxi.external_green_tripdata` LIMIT 10;

--Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table).
CREATE OR REPLACE TABLE `learn-from-datatalksclub.nytaxi.green_tripdata_non_partitoned` AS
SELECT * FROM `learn-from-datatalksclub.nytaxi.external_green_tripdata`;

-- Question 1: What is count of records for the 2022 Green Taxi Data??
select count(*) from `learn-from-datatalksclub.nytaxi.green_tripdata_non_partitoned`;
--Output 840402


-- Question 2:
-- Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
SELECT distinct(PULocationID) FROM `learn-from-datatalksclub.nytaxi.green_tripdata_non_partitoned`;
SELECT distinct(PULocationID) FROM `learn-from-datatalksclub.nytaxi.external_green_tripdata`;
--Answer: 0 MB for the External Table and 6.41MB for the Materialized Table

--Questtion 3:
-- How many records have a fare_amount of 0?
select count(*) from `learn-from-datatalksclub.nytaxi.green_tripdata_non_partitoned` where fare_amount = 0;
--Output 1622

-- Question 4:
-- What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)
CREATE OR REPLACE TABLE `learn-from-datatalksclub.nytaxi.green_tripdata_partitoned_clustered` 
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PUlocationID
AS 
SELECT * FROM `learn-from-datatalksclub.nytaxi.external_green_tripdata`;

-- Question 5:
-- Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
-- Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

SELECT DISTINCT(PULocationID) FROM `learn-from-datatalksclub.nytaxi.green_tripdata_non_partitoned`
WHERE lpep_pickup_datetime BETWEEN 
'2022-06-01 00:00:00' AND '2022-06-30 23:59:59'; 
--12.82

SELECT DISTINCT(PULocationID) FROM `learn-from-datatalksclub.nytaxi.green_tripdata_partitoned_clustered`
WHERE lpep_pickup_datetime BETWEEN 
'2022-06-01 00:00:00' AND '2022-06-30 23:59:59'; 
--1.12
-- Output: 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table

-- Question 6:
-- Where is the data stored in the External Table you created?
-- Answer: GCP bucket

-- Question 7
-- It is best practice in Big Query to always cluster your data:
-- Answer: False


-- Question 8
-- Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
-- Answer: 0B because no data will be scanned as the query can be answered by reading only metadata, rather than scanning the actual data.
