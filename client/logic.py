import base64
from os import path

import requests
from requests import Response

from client.exceptions import RequestRateException, NotFoundException

API_URL = 'https://api.spotify.com/v1/'


def check_response(response: Response):
    if response.status_code == 429:
        raise RequestRateException()
    elif response.status_code == 404:
        raise NotFoundException()


def get_access_token(client_id: str, client_secret: str) -> str:
    auth_key = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': f'Basic {auth_key}'}
    body = {'grant_type': 'client_credentials'}

    response = requests.post(url, headers=headers, data=body)

    check_response(response)

    return response.json()['access_token']


def get_search_results(access_token: str, value: str) -> dict:
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': value, 'type': 'album,artist,track'}

    response = requests.get(path.join(API_URL, 'search'), headers=headers, params=params)

    data = response.json()

    return {
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


def get_track_info(access_token: str, track_id: str) -> dict:
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(path.join(API_URL, 'tracks', track_id), headers=headers)

    check_response(response)

    data = response.json()

    return {
        'name': data['name'],
        'artist': data['artists'][0]['name'],
        'album': data['album']['name'],
    }


def get_album_info(access_token: str, album_id: str) -> dict:
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(path.join(API_URL, 'albums', album_id), headers=headers)

    check_response(response)

    data = response.json()

    return {
        'name': data['name'],
        'artist': data['artists'][0]['name'],
        'tracks': [track['name'] for track in data['tracks']['items']],
    }


def get_artist_info(access_token: str, artist_id: str) -> dict:
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(path.join(API_URL, 'artists', artist_id), headers=headers)

    check_response(response)

    data = response.json()

    return {'name': data['name'], 'genres': data['genres']}
