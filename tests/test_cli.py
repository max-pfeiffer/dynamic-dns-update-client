"""Tests for CLI."""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from click.testing import CliRunner, Result
from pytest_mock import MockerFixture

from dynamic_dns_update_client import cli
from tests.utils import FakeResponse


@pytest.mark.parametrize(
    "args",
    [
        [
            "https://example.com",
            "--ip-address-provider",
            "ipify",
            "--ip-address-url-parameter-name",
            "ip",
            "--url-parameter",
            "foo=bar",
            "--url-parameter",
            "boom=bang",
            "--url-parameter",
            "cat=mouse",
        ],
        [
            "https://example.com",
            "--ip-address-provider",
            "ipify",
            "--ip-address-url-parameter-name",
            "ip",
            "--url-parameter",
            "foo=bar",
            "--basic-auth-username",
            "username",
            "--basic-auth-password",
            "password",
        ],
        [
            "https://example.com",
            "--ip-address-provider",
            "ipify",
            "--ip-address-url-parameter-name",
            "ip",
            "--url-parameter",
            "foo=bar",
            "--dry-run",
        ],
    ],
)
def test_cli(cli_runner: CliRunner, mocker: MockerFixture, args: list[str]) -> None:
    """Test CLI.

    :param cli_runner:
    :param mocker:
    :param args:
    :return:
    """
    ip_address_response = FakeResponse("172.16.31.10", 200, False)
    mocked_ip_address_get = mocker.patch(
        "dynamic_dns_update_client.ip_address.get", return_value=ip_address_response
    )

    update_response = FakeResponse("success", 200, False)
    mocked_update_get = mocker.patch(
        "dynamic_dns_update_client.dyn_dns_update.get", return_value=update_response
    )

    result: Result = cli_runner.invoke(
        cli,
        args=args,
    )
    assert result.exit_code == 0
    mocked_ip_address_get.assert_called_once()
    if "--dry-run" in args:
        mocked_update_get.assert_not_called()
    else:
        mocked_update_get.assert_called_once()


@pytest.mark.parametrize("cache_contains_data", [True, False])
def test_cli_cache(
    cli_runner: CliRunner, mocker: MockerFixture, cache_contains_data: bool
) -> None:
    """Test CLI call with caching enabled.

    :param cli_runner:
    :param mocker:
    :param cache_contains_data:
    :return:
    """
    ip_address = "172.16.31.10"
    ip_address_response = FakeResponse(ip_address, 200, False)
    mocked_ip_address_get = mocker.patch(
        "dynamic_dns_update_client.ip_address.get", return_value=ip_address_response
    )

    update_response = FakeResponse("success", 200, False)
    mocked_update_get = mocker.patch(
        "dynamic_dns_update_client.dyn_dns_update.get", return_value=update_response
    )

    with NamedTemporaryFile() as cache_file:
        if cache_contains_data:
            with open(cache_file.name, "w") as file:
                file.write(ip_address)

        result: Result = cli_runner.invoke(
            cli,
            args=[
                "https://example.com",
                "--ip-address-provider",
                "ipify",
                "--ip-address-url-parameter-name",
                "ip",
                "--url-parameter",
                "foo=bar",
                "--cache-ip-address",
                "--cache-file",
                cache_file.name,
            ],
        )
        assert result.exit_code == 0
        assert Path(cache_file.name).read_text() == ip_address
        mocked_ip_address_get.assert_called_once()
        if cache_contains_data:
            mocked_update_get.assert_not_called()
        else:
            mocked_update_get.assert_called_once()


@pytest.mark.parametrize(
    "env",
    [
        {
            "DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_PROVIDER": "ipify",
            "DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_URL_PARAMETER_NAME": "ip",
            "DYNAMIC_DNS_UPDATE_CLIENT_URL_PARAMETER": "foo=bar",
            "DYNAMIC_DNS_UPDATE_CLIENT_BASIC_AUTH_USERNAME": "username",
            "DYNAMIC_DNS_UPDATE_CLIENT_BASIC_AUTH_PASSWORD": "password",
        },
        {
            "DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_PROVIDER": "ipify",
            "DYNAMIC_DNS_UPDATE_CLIENT_IP_ADDRESS_URL_PARAMETER_NAME": "ip",
            "DYNAMIC_DNS_UPDATE_CLIENT_URL_PARAMETER": "foo=bar boom=bang cat=mouse",
        },
    ],
)
def test_cli_with_environment_variables(
    cli_runner: CliRunner, mocker: MockerFixture, env: dict[str]
) -> None:
    """Test CLI with environment variables.

    :param cli_runner:
    :param mocker:
    :param env:
    :return:
    """
    ip_address_response = FakeResponse("172.16.31.10", 200, False)
    mocked_ip_address_get = mocker.patch(
        "dynamic_dns_update_client.ip_address.get", return_value=ip_address_response
    )

    update_response = FakeResponse("success", 200, False)
    mocked_update_get = mocker.patch(
        "dynamic_dns_update_client.dyn_dns_update.get", return_value=update_response
    )

    result: Result = cli_runner.invoke(
        cli,
        args=[
            "https://example.com",
        ],
        env=env,
    )
    assert result.exit_code == 0
    mocked_ip_address_get.assert_called_once()
    mocked_update_get.assert_called_once()
