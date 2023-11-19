import getpass

import spotipy
import keyring

_KEYRING_SERVICE_NAME = "tapslang.spotify_api"
_KEYRING_CLIENT_ID = "client_id"
_KEYRING_CLIENT_SECRET = "client_secret"


def get_songs(playlist_id):
    client_id = keyring.get_password(_KEYRING_SERVICE_NAME, _KEYRING_CLIENT_ID)
    client_secret = keyring.get_password(_KEYRING_SERVICE_NAME, "client_secret")

    if client_id is None or client_secret is None:
        print("No client ID or secret stored. Did you run `poetry run setup`?")
        exit(1)

    auth_manager = spotipy.oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist = sp.playlist(playlist_id)
    return [song["track"]["name"] for song in playlist["tracks"]["items"]]


def save_credentials():
    client_id = input("Enter Spotify client ID: ").strip()
    keyring.set_password(_KEYRING_SERVICE_NAME, _KEYRING_CLIENT_ID, client_id)
    client_secret = getpass.getpass("Enter Spotify client secret: ").strip()
    keyring.set_password(_KEYRING_SERVICE_NAME, "client_secret", client_secret)


def delete_credentials():
    keyring.delete_password(_KEYRING_SERVICE_NAME, _KEYRING_CLIENT_ID)
    keyring.delete_password(_KEYRING_SERVICE_NAME, _KEYRING_CLIENT_SECRET)


if __name__ == "__main__":
    for song in get_songs("5OHBydIdhW0KSRy3O0ghcJ"):
        print(song)
