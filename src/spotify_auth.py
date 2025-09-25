import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'https://127.0.0.1:8080'

# Define required scopes for accessing user data
SCOPE = 'user-read-private user-read-email user-library-read user-top-read user-read-recently-played playlist-read-private'


def get_spotify_client():
    """Initialize Spotify client with OAuth"""
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    return spotipy.Spotify(auth_manager=auth_manager)