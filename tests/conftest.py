"""Test fixtures."""

import pytest
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
