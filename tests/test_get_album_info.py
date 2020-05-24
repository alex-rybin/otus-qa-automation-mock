from unittest import mock

from client.logic import get_album_info
from tests.example_data import album_result


def test_returns_album_info(requests_mock):
    requests_mock.get('https://api.spotify.com/v1/albums/sample_id', text=album_result)
    result = get_album_info('sample_token', 'sample_id')
    assert result == {
        'name': 'RAMMSTEIN',
        'artist': 'Rammstein',
        'tracks': [
            'DEUTSCHLAND',
            'RADIO',
            'ZEIG DICH',
            'AUSLÄNDER',
            'SEX',
            'PUPPE',
            'WAS ICH LIEBE',
            'DIAMANT',
            'WEIT WEG',
            'TATTOO',
            'HALLOMANN',
        ],
    }


def test_calls_check_response(requests_mock):
    with mock.patch('client.logic.check_response') as check_response_mock:
        requests_mock.get('https://api.spotify.com/v1/albums/sample_id', text=album_result)
        get_album_info('sample_token', 'sample_id')
    check_response_mock.assert_called_once()
