from google.cloud import bigquery


def table_schemas(table_name) -> list:
    """
    table_name and file_name have the same value
    """
    schemas = {
        "recently_played_schema" : [
            bigquery.SchemaField("track_id", "STRING"),
            bigquery.SchemaField("track_name", "STRING"),
            bigquery.SchemaField("artist_name", "STRING"),
            bigquery.SchemaField("played_at", "TIMESTAMP"),
            bigquery.SchemaField("duration_ms", "INTEGER"),
            bigquery.SchemaField("popularity", "INTEGER"),
        ],
        "saved_tracks_schema" : [
            bigquery.SchemaField("track_id", "STRING"),
            bigquery.SchemaField("track_name", "STRING"),
            bigquery.SchemaField("artist_name", "STRING"),
            bigquery.SchemaField("artist_id", "STRING"),
            bigquery.SchemaField("album_name", "STRING"),
            bigquery.SchemaField("album_id", "STRING"),
            bigquery.SchemaField("release_date", "STRING"),
            bigquery.SchemaField("duration_ms", "INTEGER"),
            bigquery.SchemaField("popularity", "INTEGER"),
            bigquery.SchemaField("added_at", "TIMESTAMP"),
            bigquery.SchemaField("explicit", "BOOLEAN"),
        ],
        "top_artists_schema" : [
            bigquery.SchemaField("rank", "INTEGER"),
            bigquery.SchemaField("artist_id", "STRING"),
            bigquery.SchemaField("artist_name", "STRING"),
            bigquery.SchemaField("genres", "STRING"),
            bigquery.SchemaField("popularity", "INTEGER"),
            bigquery.SchemaField("followers", "INTEGER"),
            bigquery.SchemaField("time_range", "STRING"),
        ],
        "top_tracks_schema" : [
            bigquery.SchemaField("rank", "INTEGER"),
            bigquery.SchemaField("track_id", "STRING"),
            bigquery.SchemaField("track_name", "STRING"),
            bigquery.SchemaField("artist_name", "STRING"),
            bigquery.SchemaField("album_name", "STRING"),
            bigquery.SchemaField("popularity", "INTEGER"),
            bigquery.SchemaField("duration_ms", "INTEGER"),
            bigquery.SchemaField("time_range", "STRING"),
        ],
        "track_details_schema" : [
            bigquery.SchemaField("track_id", "STRING"),
            bigquery.SchemaField("track_name", "STRING"),
            bigquery.SchemaField("duration_ms", "INTEGER"),
            bigquery.SchemaField("popularity", "INTEGER"),
            bigquery.SchemaField("explicit", "BOOLEAN"),
            bigquery.SchemaField("artist_genres", "STRING"),
        ]
    }

    return schemas.get(table_name)