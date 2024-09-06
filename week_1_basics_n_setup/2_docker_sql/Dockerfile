FROM python:3.9
RUN pip install pandas sqlalchemy psycopg2

# Define build arguments
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_HOSTNAME
ARG POSTGRES_PORT

WORKDIR /app
COPY ingest_data.py ingest_data.py
COPY yellow_head.csv yellow_head.csv
ENV DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOSTNAME}:${POSTGRES_PORT}/${POSTGRES_DB}"
# ENTRYPOINT ["python", "ingest_data.py", "--database_url","$DATABASE_URL", "--table_name","yellow_taxi_trips", "--csv_url","yellow_head.csv"]
# Use the shell form of ENTRYPOINT as the environment variables are not expanded in ENTRYPOINT or CMD directly within the JSON array format. 
ENTRYPOINT python ingest_data.py --database_url "$DATABASE_URL" --table_name "yellow_taxi_trips" --csv_url "yellow_head.csv"