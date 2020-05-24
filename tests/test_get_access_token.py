from unittest import mock

from client.logic import get_access_token

RESPONSE = '{"access_token":"exampleToken","token_type":"Bearer","expires_in":3600,"scope":""}'


def test_returns_access_token(requests_mock):
    requests_mock.post('https://accounts.spotify.com/api/token', text=RESPONSE)
    result = get_access_token('sample_id', 'sample_secret')
    assert result == 'exampleToken'


def test_calls_check_response(requests_mock):
    with mock.patch('client.logic.check_response') as check_response_mock:
        requests_mock.post('https://accounts.spotify.com/api/token', text=RESPONSE)
        get_access_token('sample_id', 'sample_secret')
    check_response_mock.assert_called_once()
