from unittest import mock

from client.logic import get_track_info
from tests.example_data import track_result


def test_returns_track_info(requests_mock):
    requests_mock.get('https://api.spotify.com/v1/tracks/sample_id', text=track_result)
    result = get_track_info('sample_token', 'sample_id')
    assert result == {'name': 'TATTOO', 'artist': 'Rammstein', 'album': 'RAMMSTEIN'}


def test_calls_check_response(requests_mock):
    with mock.patch('client.logic.check_response') as check_response_mock:
        requests_mock.get('https://api.spotify.com/v1/tracks/sample_id', text=track_result)
        get_track_info('sample_token', 'sample_id')
    check_response_mock.assert_called_once()
