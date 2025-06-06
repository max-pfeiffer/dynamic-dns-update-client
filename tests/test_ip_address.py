"""Tests for obtaining current IP address."""

import pytest
from pytest_mock import MockerFixture

from dynamic_dns_update_client.ip_address import dyndns, ipfy
from tests.utils import FakeResponse


@pytest.mark.parametrize("exc", [True, False])
def test_ipfy(mocker: MockerFixture, exc: bool) -> None:
    """Test ipfy method.

    :param mocker:
    :param exc:
    :return:
    """
    response = FakeResponse("172.16.31.10", 200, exc)
    mocker.patch("dynamic_dns_update_client.ip_address.get", return_value=response)

    if exc:
        with pytest.raises(RuntimeError):
            ipfy()
    else:
        result = ipfy()
        assert result == "172.16.31.10"


@pytest.mark.parametrize("exc", [True, False])
def test_dyndns(mocker: MockerFixture, exc: bool) -> None:
    """Test dyndns method.

    :param mocker:
    :param exc:
    :return:
    """
    response = FakeResponse(
        "<html><head><title>Current IP Check</title></head>"
        "<body>Current IP Address: 178.197.185.111</body></html>\r\n",
        200,
        exc,
    )
    mocker.patch("dynamic_dns_update_client.ip_address.get", return_value=response)

    if exc:
        with pytest.raises(RuntimeError):
            dyndns()
    else:
        result = dyndns()
        assert result == "178.197.185.111"
