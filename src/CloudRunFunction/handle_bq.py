from google.cloud import bigquery
from bq_schemas import table_schemas
import pandas_gbq
import os


def move_to_bigquery(file_path, table_name):
    try:
        client = bigquery.Client()
        table_id = f"{os.environ["PROJECT_ID"]}.spotify_api_data.{table_name}"

        job_config = bigquery.LoadJobConfig(
            schema=table_schemas(table_name),
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
        )
        uri = file_path
        load_job = client.load_table_from_uri(
            uri,
            table_id,
            job_config=job_config
        )

        load_job.result()

        destination_table = client.get_table(table_id)
        print(f">> Destination_table --> {destination_table}")
        print(f">> Loaded {format(destination_table.num_rows)} rows.")
    except Exception as e:
        print(f"ERROR in move_to_bigquery: {e}")


def copy_to_bigquery(df_clean, table_name):
    table_id = f"{os.environ["PROJECT_ID"]}.spotify_api_data.{table_name}"
    try:
        pandas_gbq.to_gbq(df_clean, table_id, if_exists='append')
    except Exception as e:
        print(f"Error copy_to_bigquery: {e}")
