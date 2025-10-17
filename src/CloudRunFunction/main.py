import functions_framework
from move_bq import move_to_bigquery
import re


def get_file_name(cloud_event):
    data = cloud_event.data
    file_name = data.get("name")
    file_path = f"gs://{data.get("bucket")}/{file_name}"
    return file_path, file_name


def file_name_validation(file_path, file_name):
    name = re.findall(r"(\btrack_details)", file_name)[0]
    if name == "track_details_":
        print(f"File name to be cleaned: {file_name}")
    else:
        print(f"File name: {file_name}")
        move_to_bigquery(file_path, file_name)


@functions_framework.cloud_event
def spotify_to_bq(cloud_event):
    file_path, file_name = get_file_name(cloud_event)
    file_name_validation(file_path, file_name)
