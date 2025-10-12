from data_store import StoreDataFiles
from data_extractor import SpotifyDataExtractor
import pandas as pd


def all_spotify_data() -> dict:
    spotify_data = SpotifyDataExtractor()
    user_profile = spotify_data.get_user_profile()
    saved_tracks = spotify_data.get_saved_tracks()
    recently_played = spotify_data.get_recently_played()
    top_tracks = pd.concat([
        spotify_data.get_top_tracks('short_term'),
        spotify_data.get_top_tracks('medium_term'),
        spotify_data.get_top_tracks('long_term')
    ])
    top_artists = pd.concat([
        spotify_data.get_top_artists('short_term'),
        spotify_data.get_top_artists('medium_term'),
        spotify_data.get_top_artists('long_term')
    ])

    if not saved_tracks.empty:
        track_ids = saved_tracks['track_id'].tolist()
        track_details = spotify_data.get_track_details(track_ids)
    else:
        track_details = pd.DataFrame()

    return {
        'user_profile': user_profile,
        'saved_tracks': saved_tracks,
        'recently_played': recently_played,
        'top_tracks': top_tracks,
        'top_artists': top_artists,
        'track_details': track_details
    }


def data_to_gcs(all_data):
    store_data = StoreDataFiles(all_data, "spotify-api-data")
    store_data.save_to_gcs()


def main():
    all_data = all_spotify_data()
    data_to_gcs(all_data)


if __name__ == "__main__":
    main()