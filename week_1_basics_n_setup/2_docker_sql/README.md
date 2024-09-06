### NOTE:
Using mise for managing terraform versions and pyenv for python.

# Steps:

## 1. Creating a simple "data pipeline" in Docker
created a docker image with python and pandas installed which can accept parameters.

```
docker build -t python_pandas:latest .
docker run -it python_pandas 2024-04-09
```
## 2. Ingesting NY Taxi Data to Postgres
Then create a postgres container with the following command. I had to use the same user as host to resolve permission issues.

```
docker run -it \
    -e POSTGRES_USER="data" \
    -e POSTGRES_PASSWORD="data" \
    -e POSTGRES_DB="ny_taxi" \
    -e UID=$(id -u) \
    -e GID=$(id -g) \
    -v ./ny_taxi_data:/var/lib/postgresql/data \
    --user="${UID}:${GID}" \
    -p 5432:5432 \
    postgres:13
```
install/upgrade pgcli on local to interactive with the DB
```
pip install pgcli --upgrade pip
pgcli -h localhost -p 5432 -u data -d ny_taxi
commands to test -> \dt, \db, select 1;
```

```
pip install jupyter
pip install sqlalchemy
pip install psycopg2
```
The PostgreSQL dialect uses psycopg2 as the default DBAPI. Other PostgreSQL DBAPIs include pg8000 and asyncpg.
Ingest data in the postgres using the jupyter notebook. Refer upload-data.ipynb.

```
jupyter notebook

http://localhost:8888/tree?token=86e35d2100e4155b063b8892889ae55555feb90f12d46a3b
```

## 3. Connecting pgAdmin and Postgres containers using network
```
docker network create pg-network

docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root"  \
-p 8080:80  \
--network=pg-network    \
--name pgadmin  \
dpage/pgadmin4

docker run -it \
    -e POSTGRES_USER="data" \
    -e POSTGRES_PASSWORD="data" \
    -e POSTGRES_DB="ny_taxi" \
    -e UID=$(id -u) \
    -e GID=$(id -g) \
    -v ./ny_taxi_data:/var/lib/postgresql/data \
    --user="${UID}:${GID}" \
    -p 5432:5432 \
    --network=pg-network    \
    --name pg-database
    postgres:13

```

```
jupyter nbconvert --to=script upload-data.ipynb
add the ingest_data to the docker file and run it in the same network
docker build
docker run -t \
--user=...
--url=....
--network=...
```
## 4. Running Postgres and pgAdmin with Docker-Compose
check the docker-compose file
```
POSTGRES_PASSWORD=data UID=$(id -u) GID=$(id -g) docker-compose up --build
```
