from data_store import StoreDataFiles
from data_extractor import SpotifyDataExtractor
import pandas as pd
import time


def extract_standard_datasets(spotify_data_extractor, store_data):
    """
    For every file except <track_details> and <saved_tracks>
    In total the function store 4 files
    """
    extraction_file_tasks = [
        # Dataframe name and function
        ('user_profile', lambda: spotify_data_extractor.get_user_profile()),
        ('recently_played', lambda: spotify_data_extractor.get_recently_played()),
        ('top_tracks', lambda: pd.concat([
            spotify_data_extractor.get_top_tracks('short_term'),
            spotify_data_extractor.get_top_tracks('medium_term'),
            spotify_data_extractor.get_top_tracks('long_term')
        ])),
        ('top_artists', lambda: pd.concat([
            spotify_data_extractor.get_top_artists('short_term'),
            spotify_data_extractor.get_top_artists('medium_term'),
            spotify_data_extractor.get_top_artists('long_term')
        ]))
    ]

    for df_name, extract_func in extraction_file_tasks:
        try:
            print(f"Extracting {df_name}")
            store_data.save_to_gcs(df_name, extract_func(), "spotify-api-data-files")

        except Exception as e:
            print(f"Error: {e}")


def extract_dependent_datasets(spotify_data_extractor, store_data):
    """
    Only for <track_details> and <saved_tracks>
    In total the function store 2 files
    """
    saved_tracks = spotify_data_extractor.get_saved_tracks()
    store_data.save_to_gcs('saved_tracks', saved_tracks, "spotify-api-data-files")

    if not saved_tracks.empty:
        track_ids = saved_tracks['track_id'].tolist()
        track_details = spotify_data_extractor.get_track_details(track_ids)
        store_data.save_to_gcs('track_details', track_details, "spotify-api-data-files")
    else:
        print('>> Track_details is empty')


def extract_playlists_tracks(spotify_data_extractor, store_data, my_playlist_list):
    for playlist_id in my_playlist_list:
        try:
            print(f"Extracting tracks for playlist ID: {playlist_id}")
            playlist_tracks_df = spotify_data_extractor.get_playlist_tracks(playlist_id)

            if not playlist_tracks_df.empty:
                # Store a separate file per playlist
                file_name = f"playlist_tracks_{playlist_id}"
                store_data.save_to_gcs(file_name, playlist_tracks_df, "spotify-api-data-files")
            else:
                print(f">> No tracks found for playlist {playlist_id}")
        except Exception as e:
            print(f'Error extracting playlist {playlist_id}: {e}')

        print(f"Waiting 2 seconds before the next extraction...")
        time.sleep(10)


def spotify_etl():
    spotify_data = SpotifyDataExtractor()
    user_profile = spotify_data.get_user_profile()
    print(f"It is working {user_profile}!!!")

    spotify_data_extractor = SpotifyDataExtractor()
    store_data = StoreDataFiles()

    extract_standard_datasets(spotify_data_extractor, store_data)
    extract_dependent_datasets(spotify_data_extractor, store_data)

    my_playlist_list = [
        '2slhfhWLg1g5Sv5lkaLhRz',
        '3kMddYr1AlK1fyHROBOqMB',
        '4Kqma780gsDVuFvb8Cgio7',
        '10xYS0VnJXRrf392UMSJH1',
        '2htDErZINLpbSCD10JRAVA',
        '4EiiW94hCS7mQ7OCJyZlGM'
    ]
    extract_playlists_tracks(spotify_data_extractor, store_data, my_playlist_list)


def main():
    spotify_etl()


if __name__ == "__main__":
    main()
