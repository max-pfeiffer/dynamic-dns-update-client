"""Module for acquiring IP addresses."""

import enum
from xml.etree import ElementTree

from requests import Response, get

from dynamic_dns_update_client.constants import DYNDNS_URL, IPFY_URL


class IpAddressProviderType(enum.Enum):
    """Enum type for IP address providers."""

    IPFY = enum.auto()
    DYNDNS = enum.auto()


def ipfy() -> str:
    """Get IP address from Ipfy service.

    See: https://www.ipify.org/
    :return:
    """
    response: Response = get(IPFY_URL)
    response.raise_for_status()
    return response.text


def dyndns() -> str:
    """Get IP addresses from Oracle's DynDNS service.

    See: https://help.dyn.com/remote-access-api/checkip-tool/
    :return:
    """
    response: Response = get(DYNDNS_URL)
    response.raise_for_status()
    html = response.text.strip("\n").strip("\r")
    html_root = ElementTree.fromstring(html)
    body = html_root.find("body").text
    parts: list[str] = body.split(" ")
    return parts[3]


def get_ip_address(type: IpAddressProviderType) -> str:
    """Get IP address for a provider type.

    :param type:
    :return:
    """
    match type:
        case IpAddressProviderType.IPFY:
            return ipfy()
        case IpAddressProviderType.DYNDNS:
            return dyndns()
        case _:
            raise NotImplementedError()
