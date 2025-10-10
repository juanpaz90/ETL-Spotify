from google.cloud import storage
from datetime import datetime


class StoreDataFiles:
    def __init__(self, all_spotify_data, bucket_name: str):
        self.current_date = datetime.now().strftime("%Y%m%d")
        self.storage_client = storage.Client()
        self.all_spotify_data = all_spotify_data
        self.bucket_name = bucket_name

    def save_to_gcs(self):
        try:
            for df_name, df_data in self.all_spotify_data.items():
                csv_file_name = f'{df_name}_{self.current_date}.csv'
                bucket_destination = self.storage_client.get_bucket(self.bucket_name)

                blob = bucket_destination.blob(csv_file_name)
                blob.content_type = 'text/csv'
                df_data.to_csv(blob.open('w'), index=False)
                print(f"CSV File {csv_file_name} saved into {self.bucket_name}")

            return True
        except Exception as e:
            print(f"ERROR: {e}")