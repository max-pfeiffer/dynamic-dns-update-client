"""Tests for cache module."""

from dynamic_dns_update_client.cache import (
    read_cached_ip_address,
    write_cached_ip_address,
)


def test_cache() -> None:
    """Test the caching of the IP address.

    :return:
    """
    ip_address: str = "192.168.0.10"
    file = "/tmp/test"
    write_cached_ip_address(ip_address, cache_file=file)
    cached_ip_address = read_cached_ip_address(cache_file=file)
    assert ip_address == cached_ip_address
