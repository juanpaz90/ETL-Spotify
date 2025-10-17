import functions_framework
from handle_bq import *
from handle_data import *


def get_file_name(cloud_event):
    data = cloud_event.data
    file_name = data.get("name")
    bucket_name = data.get("bucket")
    file_path = f"gs://{bucket_name}/{file_name}"
    return file_path, file_name, bucket_name


def file_name_validation(file_path, file_name, bucket_name):
    table_name = file_name.rsplit('_', 1)[0]

    if table_name == "track_details":
        try:
            print(f"File name to be cleaned: {file_name}")
            df_data = read_file_from_gcs(bucket_name, file_name)
            df_clean = fix_genre_name(df_data)
            copy_to_bigquery(df_clean, table_name)
        except Exception as e:
            print(f"Error in File name to be cleaned: {e}")
    else:
        print(f"File name to be moved: {file_name}")
        move_to_bigquery(file_path, table_name)


@functions_framework.cloud_event
def spotify_to_bq(cloud_event):
    file_path, file_name, bucket_name = get_file_name(cloud_event)
    file_name_validation(file_path, file_name, bucket_name)
