from unittest import mock

from client.logic import get_artist_info
from tests.example_data import artist_result


def test_returns_artist_info(requests_mock):
    requests_mock.get('https://api.spotify.com/v1/artists/sample_id', text=artist_result)
    result = get_artist_info('sample_token', 'sample_id')
    assert result == {
        'name': 'Rammstein',
        'genres': [
            'alternative metal',
            'german metal',
            'industrial',
            'industrial metal',
            'industrial rock',
            'neue deutsche harte',
            'nu metal',
        ],
    }


def test_calls_check_response(requests_mock):
    with mock.patch('client.logic.check_response') as check_response_mock:
        requests_mock.get('https://api.spotify.com/v1/artists/sample_id', text=artist_result)
        get_artist_info('sample_token', 'sample_id')
    check_response_mock.assert_called_once()
