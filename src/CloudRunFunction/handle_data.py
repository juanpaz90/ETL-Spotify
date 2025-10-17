from google.cloud import storage
import pandas as pd


def read_file_from_gcs(bucket_name: str, file_name: str) -> pd.DataFrame | str:
    """Read CSV file from GCS bucket and return data as DataFrame"""
    storage_client = storage.Client()
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        return pd.read_csv(blob.open('r'))
    except Exception as e:
        print(f"ERROR: {e}")
        return 'ERROR'


def fix_genre_name(df_data):
    """Rename fields that I consider incorrect"""
    df_clean = df_data.copy()

    corrections = {
        # wrong : correct
        'tekno': 'techno'
    }

    for wrong, correct in corrections.items():
        df_clean['artist_genres'] = df_clean['artist_genres'].str.replace(
            wrong, correct, case=False, regex=False
        )

    return df_clean