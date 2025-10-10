import spotipy
from spotipy.oauth2 import SpotifyOAuth
from access_sk import SecretKey


# Define required scopes for accessing user data
SCOPE = 'user-read-private user-read-email user-library-read user-top-read user-read-recently-played playlist-read-private'
REDIRECT_URI = 'https://127.0.0.1:8080'


class SpotifyAuth:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.secret_key = SecretKey()

    def get_spotify_client(self):
        """Initialize Spotify client with OAuth"""
        auth_manager = SpotifyOAuth(
            client_id = self.secret_key.get_secret("client_id"),
            client_secret = self.secret_key.get_secret("client_secret"),
            redirect_uri=REDIRECT_URI,
            scope=SCOPE
        )

        try:
            return spotipy.Spotify(auth_manager = auth_manager)
        except Exception as e:
            print(f"ERROR: {e}")
