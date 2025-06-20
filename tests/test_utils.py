"""Tests for utilities."""

from tempfile import NamedTemporaryFile

from dynamic_dns_update_client.utils import (
    execute_cli_command,
    file_exists,
    generate_url,
)


def test_execute_cli_command() -> None:
    """Test execute_cli_command function.

    :return:
    """
    result = execute_cli_command(["echo", "test"])
    assert "test" in result


def test_file_exists() -> None:
    """Test file_exists function.

    :return:
    """
    with NamedTemporaryFile() as file:
        assert file_exists(str(file.name))
    assert not file_exists("/foo/bar")


def test_generate_url() -> None:
    """Test generate_url function.

    :return:
    """
    result = generate_url(
        "https://example.com",
        "ip",
        ["foo=bar", "boom=bang", "cat=mouse"],
        "192.168.11.11",
    )
    assert result == "https://example.com/?ip=192.168.11.11&foo=bar&boom=bang&cat=mouse"
