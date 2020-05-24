from unittest.mock import Mock

import pytest
from requests import Response

from client.exceptions import RequestRateException, NotFoundException
from client.logic import check_response


@pytest.fixture
def response_mock():
    return Mock(spec=Response)


def test_too_many_requests(response_mock):
    response_mock.status_code = 429

    with pytest.raises(RequestRateException):
        check_response(response=response_mock)


def test_not_found(response_mock):
    response_mock.status_code = 404

    with pytest.raises(NotFoundException):
        check_response(response=response_mock)
