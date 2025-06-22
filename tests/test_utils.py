"""Tests for utilities."""

from tempfile import NamedTemporaryFile

import pytest

from dynamic_dns_update_client.utils import (
    create_url_parameter,
    execute_cli_command,
    file_exists,
    generate_url,
)


def test_execute_cli_command() -> None:
    """Test execute_cli_command function.

    :return:
    """
    result = execute_cli_command("echo test")
    assert "test" in result


def test_file_exists() -> None:
    """Test file_exists function.

    :return:
    """
    with NamedTemporaryFile() as file:
        assert file_exists(str(file.name))
    assert not file_exists("/foo/bar")


@pytest.mark.parametrize(
    "ip_address_url_parameter_name,url_parameter,current_ip_address,expected_params",
    [
        (
            "ip",
            ("domain=foo.bar",),
            "192.168.127.12",
            {"ip": "192.168.127.12", "domain": "foo.bar"},
        ),
        (
            "ip",
            ("domain=foo.bar", "domain=boom.bang", "domain=cat.mouse.dog"),
            "192.168.127.12",
            {
                "ip": "192.168.127.12",
                "domain": ["foo.bar", "boom.bang", "cat.mouse.dog"],
            },
        ),
    ],
)
def test_create_url_parameter(
    ip_address_url_parameter_name: str,
    url_parameter: tuple[str],
    current_ip_address: str,
    expected_params: dict[str, str | list[str]],
) -> None:
    """Test create_url_parameter function.

    :param ip_address_url_parameter_name:
    :param url_parameter:
    :param current_ip_address:
    :param expected_params:
    :return:
    """
    params = create_url_parameter(
        ip_address_url_parameter_name, url_parameter, current_ip_address
    )
    assert params == expected_params


def test_generate_url() -> None:
    """Test generate_url function.

    :return:
    """
    result = generate_url(
        "https://example.com",
        "ip",
        ("foo=bar", "boom=bang", "cat=mouse"),
        "192.168.11.11",
    )
    assert result == "https://example.com/?ip=192.168.11.11&foo=bar&boom=bang&cat=mouse"
