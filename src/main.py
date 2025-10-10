from data_store import StoreDataFiles
from data_extractor import SpotifyDataExtractor

def main():
    spotify_data = SpotifyDataExtractor()
    all_spotify_data = spotify_data.extract_all_data()

    store_data = StoreDataFiles(all_spotify_data, "spotify_api_data")
    store_data.save_to_gcs()


    # extractor = SpotifyDataExtractor()

    # user_profile = extractor.get_user_profile()
    # print(user_profile)

    # saved_tracks = spotify_data.get_saved_tracks()
    # print(saved_tracks)

    # recently_played = extractor.get_recently_played()
    # print(recently_played)

    # top_tracks = extractor.get_top_tracks()
    # print(top_tracks)

    # top_artists = extractor.get_top_artists()
    # print(top_artists)

    # playlists = extractor.get_playlists()
    # print(playlists)

    # all_data = extractor.extract_all_data()
    # print(all_data)


if __name__ == "__main__":
    main()