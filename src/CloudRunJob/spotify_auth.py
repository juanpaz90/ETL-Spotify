import spotipy
from spotipy.oauth2 import SpotifyOAuth
from access_sk import SecretKey


# Define required scopes for accessing user data
SCOPE = 'user-read-private user-read-email user-library-read user-top-read user-read-recently-played playlist-read-private'
REDIRECT_URI = 'https://127.0.0.1:8080'


def get_spotify_client():
    """Initialize Spotify client with OAuth"""
    secret_key = SecretKey()
    spotify_refresh_token = secret_key.get_secret("spotify_refresh_token")

    auth_manager = SpotifyOAuth(
        client_id = secret_key.get_secret("spotify_client_id"),
        client_secret = secret_key.get_secret("spotify_client_secret"),
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    # WORK AROUND: I use the <token_info> & <refresh_token> to avoid the manual step required to authenticate against Spotify
    token_info = auth_manager.refresh_access_token(spotify_refresh_token)

    try:
        print("## Authentication successful!")
        return spotipy.Spotify(auth=token_info['access_token'])
    except Exception as e:
        print(f"ERROR get_spotify_client: {e}")
