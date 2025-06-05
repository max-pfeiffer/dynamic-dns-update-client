"""Tests for updating the dynamic DNS provider."""

import pytest
from pytest_mock import MockerFixture

from dynamic_dns_update_client import update_dyn_dns_provider


@pytest.mark.parametrize(
    ("basic_auth_username", "basic_auth_password"),
    [
        ("username", "password"),
        (None, None),
    ],
)
def test_update_dyn_dns_provider(
    mocker: MockerFixture, basic_auth_username: str, basic_auth_password: str
) -> None:
    """Test updating the dynamic DNS provider.

    :param mocker:
    :param basic_auth_username:
    :param basic_auth_password:
    :return:
    """
    mocked_get = mocker.patch("dynamic_dns_update_client.dyn_dns_update.get")

    dynamic_dns_provider_url: str = "https://example.com"
    ip_address_url_parameter_name: str = "ip_address"
    url_parameter: list[str] = [
        "foo=bar",
        "boom=bang",
    ]
    current_ip_address: str = "192.168.127.12"

    update_dyn_dns_provider(
        dynamic_dns_provider_url,
        ip_address_url_parameter_name,
        url_parameter,
        basic_auth_username,
        basic_auth_password,
        current_ip_address,
    )

    expected_params: dict[str, str] = {
        "foo": "bar",
        "boom": "bang",
        "ip_address": "192.168.127.12",
    }

    if basic_auth_username and basic_auth_password:
        assert mocked_get.call_args_list[0].args[0] == dynamic_dns_provider_url
        assert (
            mocked_get.call_args_list[0].kwargs["auth"].password == basic_auth_password
        )
        assert (
            mocked_get.call_args_list[0].kwargs["auth"].username == basic_auth_username
        )
        assert mocked_get.call_args_list[0].kwargs["params"] == expected_params
    else:
        assert mocked_get.call_args_list[0].args[0] == dynamic_dns_provider_url
        assert mocked_get.call_args_list[0].kwargs["params"] == expected_params
