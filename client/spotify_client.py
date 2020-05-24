import base64
from os import path

import requests
from envparse import env
from requests import Response

from client.exceptions import RequestRateException, NotFoundException

API_URL = 'https://api.spotify.com/v1/'


class SpotifyClient:
    def __init__(self):
        env.read_envfile()
        self.CLIENT_ID = env.str('CLIENT_ID')
        self.CLIENT_SECRET = env.str('CLIENT_SECRET')
        self.ACCESS_TOKEN = None
        self.login()

    def check_response(self, response: Response):
        if response.status_code == 429:
            raise RequestRateException()
        elif response.status_code == 404:
            raise NotFoundException()

    def login(self):
        auth_key = base64.b64encode(f'{self.CLIENT_ID}:{self.CLIENT_SECRET}'.encode()).decode()
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': f'Basic {auth_key}'}
        body = {'grant_type': 'client_credentials'}

        response = requests.post(url, headers=headers, data=body)

        self.check_response(response)

        self.ACCESS_TOKEN = response.json()['access_token']

    def search(self, value: str) -> dict:
        headers = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}
        params = {'q': value, 'type': 'album,artist,track'}

        response = requests.get(path.join(API_URL, 'search'), headers=headers, params=params)

        data = response.json()

        return_data = {
            'albums': [
                {'name': album['name'], 'artist': album['artists'][0]['name']}
                for album in data['albums']['items']
            ],
            'artists': [artist['name'] for artist in data['artists']['items']],
            'tracks': [
                {
                    'name': track['name'],
                    'album': track['album']['name'],
                    'artist': track['artists'][0]['name'],
                }
                for track in data['tracks']['items']
            ],
        }

        return return_data

    def get_track(self, track_id: str) -> dict:
        headers = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}

        response = requests.get(path.join(API_URL, 'tracks', track_id), headers=headers)

        self.check_response(response)

        data = response.json()

        return_data = {
            'name': data['name'],
            'artist': data['artists'][0]['name'],
            'album': data['album']['name'],
        }

        return return_data

    def get_album(self, album_id: str) -> dict:
        headers = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}

        response = requests.get(path.join(API_URL, 'albums', album_id), headers=headers)

        self.check_response(response)

        data = response.json()

        return_data = {
            'name': data['name'],
            'artist': data['artists'][0]['name'],
            'tracks': [track['name'] for track in data['tracks']['items']],
        }

        return return_data

    def get_artist(self, artist_id: str) -> dict:
        headers = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}

        response = requests.get(path.join(API_URL, 'artists', artist_id), headers=headers)

        self.check_response(response)

        data = response.json()

        return_data = {'name': data['name'], 'genres': data['genres']}

        return return_data
