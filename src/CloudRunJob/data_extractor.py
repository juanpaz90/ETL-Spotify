from spotify_auth import get_spotify_client
import pandas as pd
from datetime import datetime
import time


class SpotifyDataExtractor:
    def __init__(self):
        self.sp_client = get_spotify_client()
        self.limit = 50

    def get_user_profile(self):
        """Extract user profile information"""
        user = self.sp_client.current_user()
        my_profile_info = {
            'user_id': user['id'],
            'display_name': user['display_name'],
            'followers': user['followers']['total'],
            'country': user['country'],
            'extracted_at': datetime.now()
        }
        return pd.DataFrame([my_profile_info])

    def get_saved_tracks(self):
        """Extract the tracks that I saved"""
        tracks_data = []
        offset = 0

        while True:
            results = self.sp_client.current_user_saved_tracks(limit=self.limit, offset=offset)

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
                    'popularity': track['popularity'], # From 0 to 100, being 100 the most popular
                    'added_at': item['added_at'],
                    'explicit': track['explicit']
                })

            offset += self.limit
            print(f"Extracted {len(tracks_data)} saved tracks...")

            if len(results['items']) < self.limit:
                break

        return pd.DataFrame(tracks_data)

    def get_recently_played(self):
        """Extract my recently played tracks"""
        tracks_data = []
        results = self.sp_client.current_user_recently_played(limit=self.limit)

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

    def get_top_tracks(self, time_range):
        """Extract user's top tracks
        time_range: short_term (~4 weeks), medium_term (~6 months), long_term (~years)
        """
        tracks_data = []
        results = self.sp_client.current_user_top_tracks(time_range=time_range, limit=self.limit)

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

    def get_top_artists(self, time_range):
        """Extract my top artists"""
        artists_data = []
        results = self.sp_client.current_user_top_artists(time_range=time_range, limit=self.limit)

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

    def get_track_details(self, track_ids):
        """Get detailed track information in batches of 50 (API limit)"""
        tracks_data = []

        # Filter out None values and duplicates
        valid_track_ids = [track_id for track_id in track_ids if track_id is not None]
        valid_track_ids = list(set(valid_track_ids))

        print(f"Getting detailed info for {len(valid_track_ids)} unique tracks...")

        # Process in batches of 50 (Spotify API limit for tracks endpoint)
        for i in range(0, len(valid_track_ids), 50):
            batch_ids = valid_track_ids[i:i + 50]

            try:
                tracks = self.sp_client.tracks(batch_ids)

                for track in tracks['tracks']:
                    if track:
                        tracks_data.append({
                            'track_id': track['id'],
                            'track_name': track['name'],
                            'duration_ms': track['duration_ms'],
                            'popularity': track['popularity'],
                            'explicit': track['explicit'],
                            'artist_genres': ', '.join([genre for artist in track['artists']
                                                        for genre in self.sp_client.artist(artist['id'])['genres']])
                        })

                print(f"Batch {i // 50 + 1}: Extracted {len([t for t in tracks['tracks'] if t])} track details...")

            except Exception as e:
                print(f"Error getting track details for batch {i // 50 + 1}: {e}")
                continue

            time.sleep(0.2)  # Rate limiting

        return pd.DataFrame(tracks_data)

    def get_my_playlists_list(self):
        """Extract user's playlists"""
        playlists_data = []
        results = self.sp_client.current_user_playlists(limit=50)

        while results:
            for playlist in results['items']:
                if playlist['owner']['display_name'] == 'Juan P.':
                    playlists_data.append({
                        'playlist_id': playlist['id'],
                        'playlist_name': playlist['name'],
                        'total_tracks': playlist['tracks']['total'],
                        'public': playlist['public'],
                        'owner': playlist['owner']['display_name']
                    })
            if results['next']:
                results = self.sp_client.next(results)
            else:
                results = None

        return pd.DataFrame(playlists_data)

    def get_playlist_tracks(self, playlist_id):
        """Extract all tracks from a specific playlist"""
        tracks_data = []

        # Spotipy's playlist_items has a max limit of 100 per request
        results = self.sp_client.playlist_items(playlist_id, limit=100)

        while results:
            for item in results['items']:
                track = item.get('track')

                # Skip if track is None (can happen with local files or deleted songs)
                if not track:
                    continue

                tracks_data.append({
                    'playlist_id': playlist_id,
                    'track_id': track.get('id'),
                    'track_name': track.get('name'),
                    'artist_name': ', '.join([artist['name'] for artist in track.get('artists', [])]),
                    'artist_id': track['artists'][0]['id'] if track.get('artists') else None,
                    'album_name': track.get('album', {}).get('name'),
                    'album_id': track.get('album', {}).get('id'),
                    'release_date': track.get('album', {}).get('release_date'),
                    'duration_ms': track.get('duration_ms'),
                    'popularity': track.get('popularity'),
                    'added_at': item.get('added_at'),
                    'explicit': track.get('explicit')
                })

            # Fetch next page if available using the .next() pattern
            if results['next']:
                results = self.sp_client.next(results)
            else:
                results = None

        return pd.DataFrame(tracks_data)