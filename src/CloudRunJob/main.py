from data_store import StoreDataFiles
from data_extractor import SpotifyDataExtractor
import pandas as pd
import time
from datetime import datetime


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
            store_data.save_to_gcs(df_name, extract_func(), "spotify-api-data-files-2026")

        except Exception as e:
            print(f"Error: {e}")


def extract_dependent_datasets(spotify_data_extractor, store_data):
    """
    Only for <track_details> and <saved_tracks>
    In total the function store 2 files
    """
    saved_tracks = spotify_data_extractor.get_saved_tracks()
    store_data.save_to_gcs('saved_tracks', saved_tracks, "spotify-api-data-files-2026")

    if not saved_tracks.empty:
        track_ids = saved_tracks['track_id'].tolist()
        track_details = spotify_data_extractor.get_track_details(track_ids)
        store_data.save_to_gcs('track_details', track_details, "spotify-api-data-files-2026")
    else:
        print('>> Track_details is empty')


def extract_playlists_tracks(spotify_data_extractor, store_data, my_playlist_list):
    for playlist_id in my_playlist_list:
        try:
            print(f"Extracting tracks for playlist ID: {playlist_id}")
            playlist_tracks_df = spotify_data_extractor.get_playlist_tracks(playlist_id)
            store_data.save_to_gcs(f'playlist_tracks_{playlist_id}', playlist_tracks_df, "spotify-api-data-files-2026")

            if not playlist_tracks_df.empty:
                track_ids = playlist_tracks_df['track_id'].tolist()
                track_details = spotify_data_extractor.get_track_details(track_ids)
                store_data.save_to_gcs(f'playlist_tracks_details_{playlist_id}', track_details, "spotify-api-data-files-2026")
            else:
                print(f">> No tracks found for playlist {playlist_id}")
        except Exception as e:
            print(f'Error extracting playlist {playlist_id}: {e}')

        print(f"Waiting 10 seconds before the next extraction...")
        time.sleep(30)


def get_track_details_from_local_file(spotify_data_extractor, store_data):
    """ It only works and should be used LOCALLY """
    data_path = '/Users/juanpazmino/Documents/Desarrollo/Personal_projects/SpotifyDataVis/data/2026/'
    df_saved_tracks = pd.read_csv(f'{data_path}saved_tracks_20260315.csv')
    df_saved_tracks['added_at'] = pd.to_datetime(df_saved_tracks['added_at'])

    # Getting only tracks that I need.
    start_date = datetime.fromisoformat('2025-10-17T20:33:46+00:00')
    filtered_df_saved_tracks_26 = df_saved_tracks.loc[(df_saved_tracks['added_at'] >= start_date)]
    print(filtered_df_saved_tracks_26)


    if not filtered_df_saved_tracks_26.empty:
        track_ids = filtered_df_saved_tracks_26['track_id'].tolist()
        print(track_ids)
        print(f'Length: {len(track_ids)}')
        track_details = spotify_data_extractor.get_track_details(track_ids)
        store_data.save_to_gcs('track_details_2026', track_details, "spotify-api-data-files-2026")
    else:
        print('>> Track_details is empty')


def spotify_etl():
    # spotify_data = SpotifyDataExtractor()
    # user_profile = spotify_data.get_user_profile()
    # print(f"It is working {user_profile}!!!")

    spotify_data_extractor = SpotifyDataExtractor()
    store_data = StoreDataFiles()

    # extract_standard_datasets(spotify_data_extractor, store_data)
    # extract_dependent_datasets(spotify_data_extractor, store_data) # All tracks and their details
    # get_track_details_from_local_file(spotify_data_extractor, store_data)

    my_playlist_list = [
        # '2slhfhWLg1g5Sv5lkaLhRz',
        # '3kMddYr1AlK1fyHROBOqMB',
        # '4Kqma780gsDVuFvb8Cgio7',
        '10xYS0VnJXRrf392UMSJH1',
        '2htDErZINLpbSCD10JRAVA',
        '4EiiW94hCS7mQ7OCJyZlGM'
    ]
    extract_playlists_tracks(spotify_data_extractor, store_data, my_playlist_list)


def main():
    spotify_etl()


if __name__ == "__main__":
    main()
