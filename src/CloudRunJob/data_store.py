from google.cloud import storage
from datetime import datetime


class StoreDataFiles:
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y%m%d")
        self.storage_client = storage.Client()

    def save_to_gcs(self, df_name: str, df_data, bucket_name:str):
        try:
            csv_file_name = f'{df_name}_{self.current_date}.csv'
            bucket_destination = self.storage_client.get_bucket(bucket_name)

            blob = bucket_destination.blob(csv_file_name)
            blob.content_type = 'text/csv'
            df_data.to_csv(blob.open('w'), index=False)
            print(f"CSV File {csv_file_name} saved into {bucket_name}")

            return True
        except Exception as e:
            print(f"ERROR save_to_gcs: {e}")