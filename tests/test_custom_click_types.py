"""Tests for custom click types."""

import click
import pytest

from dynamic_dns_update_client.types import UrlParameterType, UrlType


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        ("http://www.example.com", True),
        ("http://www.example.com/", True),
        ("http://www.example.com:8080", True),
        ("http:/www.example.com/", False),
        ("http//www.example.com/", False),
    ],
)
def test_url_type(value: str, valid: bool) -> None:
    """Test UrlTupe.

    :param value:
    :param valid:
    :return:
    """
    if valid:
        assert UrlType().convert(value, None, None)
    else:
        with pytest.raises(click.BadParameter):
            UrlType().convert(value, None, None)


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        ("foo=bar", True),
        ("foo=", False),
        ("=bar", False),
        ("foobar", False),
    ],
)
def test_url_parameter_type(value: str, valid: bool) -> None:
    """Test UrlParameterType.

    :param value:
    :param valid:
    :return:
    """
    if valid:
        assert UrlParameterType().convert(value, None, None)
    else:
        with pytest.raises(click.BadParameter):
            UrlParameterType().convert(value, None, None)
