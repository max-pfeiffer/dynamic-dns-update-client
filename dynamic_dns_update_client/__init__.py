"""Command line interface."""

import click

from dynamic_dns_update_client.ip_address import IpAddressProviderType, get_ip_address
from dynamic_dns_update_client.types import UrlParameterType, UrlType


@click.command()
@click.argument(
    "dynamic_dns_provider_url",
    type=UrlType(),
    required=True,
)
@click.option(
    "--ip-address-provider",
    type=click.Choice(IpAddressProviderType, case_sensitive=False),
    default=IpAddressProviderType.IPFY,
    help=f"Type of IP address provider. Default: {IpAddressProviderType.IPFY.value}",
)
@click.option(
    "--ip-address-url-parameter",
    required=True,
    help="Name of the URL parameter for IP address. "
    "It will be appended to the dynamic DNS provider URL.",
)
@click.option(
    "--url-parameter",
    type=UrlParameterType(),
    multiple=True,
    help="URL parameter which will be appended to the dynamic DNS provider URL. "
    "Format: param=value",
)
@click.option(
    "--basic-auth-username",
    help="Basic Auth username for calling dynamic DNS provider URL.",
)
@click.option(
    "--basic-auth-password",
    help="Basic Auth password for calling dynamic DNS provider URL.",
)
def cli(
    dynamic_dns_provider_url: str,
    ip_address_provider: IpAddressProviderType,
    ip_address_url_parameter: str,
    url_parameter: list[str],
    basic_auth_username: str,
    basic_auth_password: str,
) -> None:
    """Dynamic DNS Update Client CLI interface.

    :param dynamic_dns_provider_url:
    :param ip_address_provider:
    :param ip_address_url_parameter:
    :param url_parameter:
    :param basic_auth_username:
    :param basic_auth_password:
    :return:
    """
    current_ip_address: str = get_ip_address(ip_address_provider)
    click.echo(f"Current IP address: {current_ip_address}")
