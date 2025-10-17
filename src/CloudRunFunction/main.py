import functions_framework
from handle_bq import *
import re
from handle_data import *


def get_file_name(cloud_event):
    data = cloud_event.data
    file_name = data.get("name")
    bucket_name = data.get("bucket")
    file_path = f"gs://{bucket_name}/{file_name}"
    return file_path, file_name, bucket_name


def file_name_validation(file_path, file_name, bucket_name):
    # table_name and file_name have the same name, so I can use them without any problem
    name = re.findall(r"(\btrack_details)", file_name)
    try:
        if name[0] == "track_details":
            print(f"File name to be cleaned: {file_name}")
            df_data = read_file_from_gcs(bucket_name, file_name)
            df_clean = fix_genre_name(df_data)
            copy_to_bigquery(df_clean, file_name)
        else:
            print(f"File name: {file_name}")
            move_to_bigquery(file_path, file_name)
    except Exception as e:
        print(f"ERROR: {e}")


@functions_framework.cloud_event
def spotify_to_bq(cloud_event):
    file_path, file_name, bucket_name = get_file_name(cloud_event)
    file_name_validation(file_path, file_name, bucket_name)
