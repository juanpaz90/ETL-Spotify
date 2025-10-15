import pandas as pd
import pandas_gbq

def get_bucket_name(event):
    name = event['name']
    bucket = event['bucket']
    return f"gs://{bucket}/{name}"


def copy_to_bigquery(data_frame):
    table_id = f"techops-cloud-operations.ccf.ccf_complete_dataset"
    df = pd.DataFrame(data_frame)
    try:
        pandas_gbq.to_gbq(df, table_id, if_exists='append')
        print(f"SUCCESS - Data transferred to {table_id}")
    except Exception as e:
        print(f"ERROR - {e}")