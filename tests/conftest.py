"""Test fixtures."""

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="session")
def cli_runner() -> CliRunner:
    """CLI runner for testing click CLI.

    :return:
    """
    runner = CliRunner()
    return runner
