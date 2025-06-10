"""Tests for obtaining current IP address."""

import pytest
from pytest_mock import MockerFixture

from dynamic_dns_update_client.ip_address import dyndns, interface, ipfy
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
            ipfy(False)
    else:
        result = ipfy(False)
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
            dyndns(False)
    else:
        result = dyndns(False)
        assert result == "178.197.185.111"


@pytest.mark.parametrize("ipv6", [True, False])
def test_interface(mocker: MockerFixture, ifconfig_output: str, ipv6: bool) -> None:
    """Test interface method.

    :param mocker:
    """
    mocked_execute_cli_command = mocker.patch(
        "dynamic_dns_update_client.ip_address.execute_cli_command",
        return_value=ifconfig_output,
    )
    result = interface("en0", ipv6)

    mocked_execute_cli_command.assert_called_once()
    if ipv6:
        assert result == "fe80::4b4:abb1:e8e0:214a"
    else:
        assert result == "172.18.239.87"
