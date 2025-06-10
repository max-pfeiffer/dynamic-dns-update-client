"""Module for acquiring IP addresses."""

import enum
from subprocess import CalledProcessError
from xml.etree import ElementTree

import click
from requests import Response, get

from dynamic_dns_update_client.constants import DYNDNS_URL, IPIFY_URL, IPIFY_V6_URL
from dynamic_dns_update_client.utils import cli_command_exists, execute_cli_command


class IpAddressProviderType(enum.Enum):
    """Enum type for IP address providers."""

    NETWORK = "network"
    INTERFACE = "interface"
    IPFY = "ipfy"
    DYNDNS = "dyndns"


def network(ip_network: str, ipv6: bool) -> str:
    """Get IP address for a network.

    This only works on an OpenWRT machine as we are calling OpenWRT
    specific functions here.

    :param ip_network:
    :param ipv6:
    :return:
    """
    if ipv6:
        openwrt_function = "network_get_ipaddr6"
    else:
        openwrt_function = "network_get_ipaddr"

    if cli_command_exists(openwrt_function):
        arguments = [openwrt_function, ip_network]
        try:
            result: str = execute_cli_command(arguments)
            return result
        except CalledProcessError as exc:
            raise click.ClickException(f"Error executing: {arguments}") from exc
    else:
        raise click.BadOptionUsage(
            "--ip-address-provider",
            "You can use the network IP address provider only on a OpenWRT machine.",
        )


def interface(ip_interface: str, ipv6: bool) -> str:
    """Get IP address from a physical interface.

    :param ip_interface:
    :param ipv6:
    :return:
    """
    if cli_command_exists("ip"):
        arguments = ["ip", "-o", "addr", "show", "dev", ip_interface, "scope", "global"]
        try:
            result: str = execute_cli_command(arguments)
            return result
        except CalledProcessError as exc:
            raise click.ClickException(f"Error executing: {arguments}") from exc
    else:
        # If ip command is not available, we need to use the deprecated ifconfig command
        arguments = ["ifconfig", ip_interface]
        if ipv6:
            inet = "inet6"
        else:
            inet = "inet"

        try:
            result = execute_cli_command(arguments)
            for line in result.splitlines():
                parts = line.strip().split(" ")
                if parts[0] == inet:
                    ip_address = parts[1]
                    return ip_address
            raise click.ClickException("Cannot find IP address in ifconfig output.")
        except CalledProcessError as exc:
            raise click.ClickException(f"Error executing: {arguments}") from exc


def ipfy(ipv6: bool) -> str:
    """Get IP address from Ipfy service.

    See: https://www.ipify.org/

    :param ipv6:
    :return:
    """
    if ipv6:
        url = IPIFY_V6_URL
    else:
        url = IPIFY_URL
    response: Response = get(url)
    response.raise_for_status()
    return response.text


def dyndns(ipv6: bool) -> str:
    """Get IP addresses from Oracle's DynDNS service.

    See: https://help.dyn.com/remote-access-api/checkip-tool/

    :param ipv6:
    :return:
    """
    if ipv6:
        raise click.BadOptionUsage(
            "--ipv6", "IPv6 is not supported with this IP address provider."
        )

    response: Response = get(DYNDNS_URL)
    response.raise_for_status()
    html = response.text.strip("\n").strip("\r")
    html_root = ElementTree.fromstring(html)
    body = html_root.find("body").text
    parts: list[str] = body.split(" ")
    return parts[3]


def get_ip_address(
    type: IpAddressProviderType, ip_network: str, ip_interface: str, ipv6: bool
) -> str:
    """Get IP address for a provider type.

    :param type:
    :param ip_network:
    :param ip_interface:
    :param ipv6:
    :return:
    """
    match type:
        case IpAddressProviderType.NETWORK:
            return network(ip_network, ipv6)
        case IpAddressProviderType.INTERFACE:
            return interface(ip_interface, ipv6)
        case IpAddressProviderType.IPFY:
            return ipfy(ipv6)
        case IpAddressProviderType.DYNDNS:
            return dyndns(ipv6)
        case _:
            raise NotImplementedError()
