from unittest import mock

from client.logic import get_search_results
from tests.example_data import search_response, expected_search_result


def test_returns_search_results(requests_mock):
    requests_mock.get('https://api.spotify.com/v1/search', text=search_response)
    result = get_search_results('sample_token', 'Twisted')
    assert result == expected_search_result


def test_calls_check_response(requests_mock):
    with mock.patch('client.logic.check_response') as check_response_mock:
        requests_mock.get('https://api.spotify.com/v1/search', text=search_response)
        get_search_results('sample_token', 'Twisted')
    check_response_mock.assert_called_once()
