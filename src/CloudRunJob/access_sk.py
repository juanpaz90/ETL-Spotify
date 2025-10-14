import os
from google.cloud import secretmanager


class SecretKey:
    def __init__(self):
        self.my_project_id = os.environ["PROJECT_ID"]
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, key_name) -> str | None:
        secret_name = f"projects/{self.my_project_id}/secrets/{key_name}/versions/latest"
        try:
            response = self.client.access_secret_version(name=secret_name)
            # --> access_secret_version
            my_secret_value = response.payload.data.decode("UTF-8")
            return my_secret_value
        except Exception as e:
            print(f"Error: {e}")
