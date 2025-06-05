"""Command line interface."""

# ruff: noqa: D301, D401

import click

from dynamic_dns_update_client.dyn_dns_update import update_dyn_dns_provider
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
    "--ip-address-url-parameter-name",
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
    ip_address_url_parameter_name: str,
    url_parameter: list[str],
    basic_auth_username: str,
    basic_auth_password: str,
) -> None:
    """Dynamic DNS Update Client.

    A CLI tool for updating the IP address for dynamic DNS providers.
    It obtains the current IP address by calling one the following IP address services
    using a HTTP GET request:

    - ipfy: https://www.ipify.org/

    - dyndns: https://help.dyn.com/remote-access-api/checkip-tool/

    It then updates the obtained IP address with another HTTP GET request at the dynamic
    DNS provider using the specified URL parameters and authentication method.

    \f

    :param dynamic_dns_provider_url:
    :param ip_address_provider:
    :param ip_address_url_parameter_name:
    :param url_parameter:
    :param basic_auth_username:
    :param basic_auth_password:
    :return:
    """
    if basic_auth_username and basic_auth_password is None:
        raise click.BadOptionUsage(
            "--basic-auth-password", "Please specify also a Basic Auth password."
        )
    if basic_auth_password and basic_auth_username is None:
        raise click.BadOptionUsage(
            "--basic-auth-username", "Please specify also a Basic Auth username."
        )

    current_ip_address: str = get_ip_address(ip_address_provider)
    click.echo(f"Current IP address: {current_ip_address}")

    update_dyn_dns_provider(
        dynamic_dns_provider_url,
        ip_address_url_parameter_name,
        url_parameter,
        basic_auth_username,
        basic_auth_password,
        current_ip_address,
    )
    click.echo("The IP address was successfully updated at the dynamic DNS provider.")
