import spotipy
import pandas as pd
from datetime import datetime
import time
from spotify_auth import get_spotify_client


class SpotifyDataExtractor:
    def __init__(self):
        self.sp = get_spotify_client()
        self.user_id = self.sp.current_user()['id']
        print(f"Authenticated as: {self.sp.current_user()['display_name']}")

    def get_user_profile(self):
        """Extract user profile information"""
        user = self.sp.current_user()
        return {
            'user_id': user['id'],
            'display_name': user['display_name'],
            'followers': user['followers']['total'],
            'country': user['country'],
            'extracted_at': datetime.now()
        }

    def get_saved_tracks(self, limit=50):
        """Extract user's saved tracks (liked songs)"""
        tracks_data = []
        offset = 0

        while True:
            results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)

            if not results['items']:
                break

            for item in results['items']:
                track = item['track']
                tracks_data.append({
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
                    'artist_id': track['artists'][0]['id'],
                    'album_name': track['album']['name'],
                    'album_id': track['album']['id'],
                    'release_date': track['album']['release_date'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'added_at': item['added_at'],
                    'explicit': track['explicit']
                })

            offset += limit
            print(f"Extracted {len(tracks_data)} saved tracks...")

            if len(results['items']) < limit:
                break

        return pd.DataFrame(tracks_data)

    def get_recently_played(self, limit=50):
        """Extract recently played tracks"""
        tracks_data = []

        results = self.sp.current_user_recently_played(limit=limit)

        for item in results['items']:
            track = item['track']
            tracks_data.append({
                'track_id': track['id'],
                'track_name': track['name'],
                'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
                'played_at': item['played_at'],
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity']
            })

        return pd.DataFrame(tracks_data)

    def get_top_tracks(self, time_range='medium_term', limit=50):
        """Extract user's top tracks
        time_range: short_term (~4 weeks), medium_term (~6 months), long_term (~years)
        """
        tracks_data = []

        results = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)

        for idx, track in enumerate(results['items']):
            tracks_data.append({
                'rank': idx + 1,
                'track_id': track['id'],
                'track_name': track['name'],
                'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
                'album_name': track['album']['name'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'time_range': time_range
            })

        return pd.DataFrame(tracks_data)

    def get_top_artists(self, time_range='medium_term', limit=50):
        """Extract user's top artists"""
        artists_data = []

        results = self.sp.current_user_top_artists(time_range=time_range, limit=limit)

        for idx, artist in enumerate(results['items']):
            artists_data.append({
                'rank': idx + 1,
                'artist_id': artist['id'],
                'artist_name': artist['name'],
                'genres': ', '.join(artist['genres']),
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'time_range': time_range
            })

        return pd.DataFrame(artists_data)

    def get_playlists(self, limit=50):
        """Extract only the playlists that I created"""
        playlists_data = []
        offset = 0

        while True:
            results = self.sp.user_playlists(self.user_id, limit=limit, offset=offset)

            if not results['items']:
                break

            for playlist in results['items']:
                # Only include playlists owned by the user
                if playlist['owner']['id'] == self.user_id:
                    playlists_data.append({
                        'playlist_id': playlist['id'],
                        'playlist_name': playlist['name'],
                        'description': playlist['description'],
                        'total_tracks': playlist['tracks']['total'],
                        'public': playlist['public'],
                        'collaborative': playlist['collaborative'],
                        'owner': playlist['owner']['display_name']
                    })

            offset += limit
            print(f"Extracted {len(playlists_data)} owned playlists...")

            if len(results['items']) < limit:
                break

        return pd.DataFrame(playlists_data)

    def get_audio_features(self, track_ids):
        """Get audio features for tracks (in batches of 100)"""
        features_data = []

        # Filter out None values and duplicates
        valid_track_ids = [track_id for track_id in track_ids if track_id is not None]
        valid_track_ids = list(set(valid_track_ids))  # Remove duplicates

        print(f"Getting audio features for {len(valid_track_ids)} unique tracks...")

        # Process in batches of 100 (Spotify API limit)
        for i in range(0, len(valid_track_ids), 100):
            batch_ids = valid_track_ids[i:i+100]

            try:
                features = self.sp.audio_features(batch_ids)

                for feature in features:
                    if feature:  # Some tracks might not have audio features
                        features_data.append({
                            'track_id': feature['id'],
                            'danceability': feature['danceability'],
                            'energy': feature['energy'],
                            'key': feature['key'],
                            'loudness': feature['loudness'],
                            'mode': feature['mode'],
                            'speechiness': feature['speechiness'],
                            'acousticness': feature['acousticness'],
                            'instrumentalness': feature['instrumentalness'],
                            'liveness': feature['liveness'],
                            'valence': feature['valence'],
                            'tempo': feature['tempo'],
                            'time_signature': feature['time_signature']
                        })

                print(f"Batch {i//100 + 1}: Extracted {len([f for f in features if f])} audio features...")

            except Exception as e:
                print(f"Error getting audio features for batch {i//100 + 1}: {e}")
                print(f"Problematic track IDs: {batch_ids[:5]}...")  # Show first 5 IDs
                continue

            time.sleep(0.2)  # Increased delay to avoid rate limiting

        return pd.DataFrame(features_data)

    def extract_all_data(self):
        """Extract all user data"""
        print("Starting data extraction...")

        # Extract all data
        user_profile = self.get_user_profile()
        saved_tracks = self.get_saved_tracks()
        recently_played = self.get_recently_played()
        top_tracks_short = self.get_top_tracks('short_term')
        top_tracks_medium = self.get_top_tracks('medium_term')
        top_tracks_long = self.get_top_tracks('long_term')
        top_artists_short = self.get_top_artists('short_term')
        top_artists_medium = self.get_top_artists('medium_term')
        top_artists_long = self.get_top_artists('long_term')
        playlists = self.get_playlists()

        # Get audio features for saved tracks
        if not saved_tracks.empty:
            track_ids = saved_tracks['track_id'].tolist()
            audio_features = self.get_audio_features(track_ids)
        else:
            audio_features = pd.DataFrame()

        # Save to CSV files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        saved_tracks.to_csv(f'spotify_saved_tracks_{timestamp}.csv', index=False)
        recently_played.to_csv(f'spotify_recently_played_{timestamp}.csv', index=False)
        pd.concat([top_tracks_short, top_tracks_medium, top_tracks_long]).to_csv(f'spotify_top_tracks_{timestamp}.csv',
                                                                                 index=False)
        pd.concat([top_artists_short, top_artists_medium, top_artists_long]).to_csv(
            f'spotify_top_artists_{timestamp}.csv', index=False)
        playlists.to_csv(f'spotify_playlists_{timestamp}.csv', index=False)
        audio_features.to_csv(f'spotify_audio_features_{timestamp}.csv', index=False)

        print(f"\nExtraction completed!")
        print(f"Saved tracks: {len(saved_tracks)}")
        print(f"Recently played: {len(recently_played)}")
        print(f"Top tracks: {len(pd.concat([top_tracks_short, top_tracks_medium, top_tracks_long]))}")
        print(f"Top artists: {len(pd.concat([top_artists_short, top_artists_medium, top_artists_long]))}")
        print(f"Playlists: {len(playlists)}")
        print(f"Audio features: {len(audio_features)}")

        return {
            'user_profile': user_profile,
            'saved_tracks': saved_tracks,
            'recently_played': recently_played,
            'top_tracks': pd.concat([top_tracks_short, top_tracks_medium, top_tracks_long]),
            'top_artists': pd.concat([top_artists_short, top_artists_medium, top_artists_long]),
            'playlists': playlists,
            'audio_features': audio_features
        }


# if __name__ == "__main__":
#     extractor = SpotifyDataExtractor()
#     data = extractor.extract_all_data()