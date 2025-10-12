import spotipy
from spotipy.oauth2 import SpotifyOAuth
from access_sk import SecretKey


# Define required scopes for accessing user data
SCOPE = 'user-read-private user-read-email user-library-read user-top-read user-read-recently-played playlist-read-private'
REDIRECT_URI = 'https://127.0.0.1:8080'


def get_spotify_client():
    """Initialize Spotify client with OAuth"""
    secret_key = SecretKey()

    auth_manager = SpotifyOAuth(
        client_id = secret_key.get_secret("spotify_client_id"),
        client_secret = secret_key.get_secret("spotify_client_secret"),
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    try:
        print("## Authentication successful!")
        return spotipy.Spotify(auth_manager = auth_manager)
    except Exception as e:
        print(f"ERROR: {e}")
