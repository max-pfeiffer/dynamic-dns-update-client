"""Test fixtures."""

import pytest
from _pytest.fixtures import SubRequest
from click.testing import CliRunner


@pytest.fixture(scope="session")
def cli_runner() -> CliRunner:
    """CLI runner for testing click CLI.

    :return:
    """
    runner = CliRunner()
    return runner


@pytest.fixture(scope="session")
def ifconfig_output() -> str:
    """Ifconfig stdout.

    :return:
    """
    return """en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6460<TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether 4a:f8:2e:82:e8:f8
	inet6 fe80::4b4:abb1:e8e0:214a prefixlen 64 secured scopeid 0xf
	inet 172.18.239.87 netmask 0xffff0000 broadcast 172.18.255.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
    """


@pytest.fixture(scope="session")
def ip_output() -> str:
    """Ip stdout.

    :return:
    """
    return (
        "7: wan    inet 192.168.0.10/24 brd 192.168.0.255 scope global wan\\       "
        "valid_lft forever preferred_lft forever\n"
        "7: wan    inet6 2a02:1210:5207:3100:1491:82ff:fe2e:2489/64 scope global"
        " dynamic noprefixroute \\       valid_lft 21549sec preferred_lft 7149sec\n"
    )


@pytest.fixture(scope="function")
def openwrt_test_data(request: SubRequest) -> tuple[str, bool]:
    """OpenWRT function output."""
    if request.param:
        return "2a02:1210:5207:3100:1491:82ff:fe2e:2489", request.param
    else:
        return "192.168.0.10", request.param
