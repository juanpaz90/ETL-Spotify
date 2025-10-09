import pandas as pd
from datetime import datetime
import time
from spotify_auth import get_spotify_client
from dataclasses import dataclass


@dataclass
class SpotifyDataExtractor:
    sp_client = get_spotify_client()
    user_id = sp_client.current_user()['id']

    def get_user_profile(self):
        """Extract user profile information"""
        user = self.sp_client.current_user()
        return {
            'user_id': user['id'],
            'display_name': user['display_name'],
            'followers': user['followers']['total'],
            'country': user['country'],
            'extracted_at': datetime.now()
        }

    def get_saved_tracks(self, limit=50):
        """Extract the tracks that I saved"""
        tracks_data = []
        offset = 0

        while True:
            results = self.sp_client.current_user_saved_tracks(limit=limit, offset=offset)

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

            offset += limit
            print(f"Extracted {len(tracks_data)} saved tracks...")

            if len(results['items']) < limit:
                break

        return pd.DataFrame(tracks_data)

    def get_recently_played(self, limit=50):
        """Extract my recently played tracks"""
        tracks_data = []
        results = self.sp_client.current_user_recently_played(limit=limit)

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
        results = self.sp_client.current_user_top_tracks(time_range=time_range, limit=limit)

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
        """Extract my top artists"""
        artists_data = []
        results = self.sp_client.current_user_top_artists(time_range=time_range, limit=limit)

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
            results = self.sp_client.user_playlists(self.user_id, limit=limit, offset=offset)

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

    # TODO move this method to a new Class
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

        # Get detailed track information instead of audio features
        if not saved_tracks.empty:
            track_ids = saved_tracks['track_id'].tolist()
            # Debug: Check for invalid track IDs
            print(f"Total track IDs: {len(track_ids)}")
            print(f"None values: {track_ids.count(None)}")
            print(f"Sample track IDs: {[id for id in track_ids[:5] if id is not None]}")

            track_details = self.get_track_details(track_ids)
        else:
            track_details = pd.DataFrame()

        # Save to CSV files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        saved_tracks.to_csv(f'spotify_saved_tracks_{timestamp}.csv', index=False)
        recently_played.to_csv(f'spotify_recently_played_{timestamp}.csv', index=False)
        pd.concat([top_tracks_short, top_tracks_medium, top_tracks_long]).to_csv(f'spotify_top_tracks_{timestamp}.csv',
                                                                                 index=False)
        pd.concat([top_artists_short, top_artists_medium, top_artists_long]).to_csv(
            f'spotify_top_artists_{timestamp}.csv', index=False)
        playlists.to_csv(f'spotify_playlists_{timestamp}.csv', index=False)
        track_details.to_csv(f'spotify_track_details_{timestamp}.csv', index=False)

        print(f"\nExtraction completed!")
        print(f"Saved tracks: {len(saved_tracks)}")
        print(f"Recently played: {len(recently_played)}")
        print(f"Top tracks: {len(pd.concat([top_tracks_short, top_tracks_medium, top_tracks_long]))}")
        print(f"Top artists: {len(pd.concat([top_artists_short, top_artists_medium, top_artists_long]))}")
        print(f"Playlists: {len(playlists)}")
        print(f"Track details: {len(track_details)}")

        return {
            'user_profile': user_profile,
            'saved_tracks': saved_tracks,
            'recently_played': recently_played,
            'top_tracks': pd.concat([top_tracks_short, top_tracks_medium, top_tracks_long]),
            'top_artists': pd.concat([top_artists_short, top_artists_medium, top_artists_long]),
            'playlists': playlists,
            'track_details': track_details
        }


# if __name__ == "__main__":
#     extractor = SpotifyDataExtractor()
#     data = extractor.extract_all_data()