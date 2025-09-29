from extractor import *

def main():
    extractor = SpotifyDataExtractor()

    # user_profile = extractor.get_user_profile()
    # print(user_profile)

    # saved_tracks = extractor.get_saved_tracks()
    # print(saved_tracks)

    # recently_played = extractor.get_recently_played()
    # print(recently_played)

    # top_tracks = extractor.get_top_tracks()
    # print(top_tracks)

    # top_artists = extractor.get_top_artists()
    # print(top_artists)

    # playlists = extractor.get_playlists()
    # print(playlists)

    all_data = extractor.extract_all_data()
    print(all_data)






    # if not saved_tracks.empty:
    #     tracks_id = saved_tracks['track_id'].tolist()
    #     audio_features =extractor.get_audio_features(tracks_id)
    #     # print(tracks_id)
    #     # print(len(tracks_id))
    # else:
    #     audio_features = pd.DataFrame()
    #     print(audio_features)


if __name__ == "__main__":
    main()