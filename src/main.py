from spotify_auth import *

def main():
    sp = get_spotify_client()

    # Test authentication by getting user profile
    user = sp.current_user()
    print(f"Authenticated as: {user['display_name']}")
    print(f"User ID: {user['id']}")
    print(f"Followers: {user['followers']['total']}")

if __name__ == "__main__":
    main()