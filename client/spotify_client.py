from envparse import env

from client.logic import (
    get_access_token,
    get_search_results,
    get_track_info,
    get_album_info,
    get_artist_info,
)


class SpotifyClient:
    def __init__(self):
        env.read_envfile()
        self.CLIENT_ID = env.str('CLIENT_ID')
        self.CLIENT_SECRET = env.str('CLIENT_SECRET')
        self.ACCESS_TOKEN = None
        self.login()

    def login(self):
        self.ACCESS_TOKEN = get_access_token(self.CLIENT_ID, self.CLIENT_SECRET)

    def search(self, value: str) -> dict:
        return get_search_results(self.ACCESS_TOKEN, value)

    def get_track(self, track_id: str) -> dict:
        return get_track_info(self.ACCESS_TOKEN, track_id)

    def get_album(self, album_id: str) -> dict:
        return get_album_info(self.ACCESS_TOKEN, album_id)

    def get_artist(self, artist_id: str) -> dict:
        return get_artist_info(self.ACCESS_TOKEN, artist_id)
