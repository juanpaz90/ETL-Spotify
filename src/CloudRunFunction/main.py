import pandas as pd
import pandas_gbq

def get_bucket_name(event):
    name = event['name']
    bucket = event['bucket']
    return f"gs://{bucket}/{name}"


def copy_to_bigquery(data_frame):
    recently_played = f"gen-lang-client-0386264733.spotify_api_data.recently_played"
    saved_tracks = f"gen-lang-client-0386264733.spotify_api_data.saved_tracks"
    top_artists = f"gen-lang-client-0386264733.spotify_api_data.top_artists"
    top_tracks = f"gen-lang-client-0386264733.spotify_api_data.top_tracks"
    track_details = f"gen-lang-client-0386264733.spotify_api_data.track_details"

    df = pd.DataFrame(data_frame)
    try:
        # TODO update the logic to capture file name, and use it as a variable name
        pandas_gbq.to_gbq(df, table_id, if_exists='append')
        print(f"SUCCESS - Data transferred to {table_id}")
    except Exception as e:
        print(f"ERROR - {e}")


def spotify_to_bq(event, context):
    get_bucket_name(event)