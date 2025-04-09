import pytest
from dotenv import load_dotenv


"""
This module contains pytest fixtures for loading environment variables.

Fixtures:
    load_env (function): A session-scoped, automatically used fixture that loads
    environment variables from a .env file using the `load_dotenv` function from
    the `dotenv` package.
"""


@pytest.fixture(scope='session', autouse=True)
def load_env():
    """
    Automatically loads environment variables from a .env file at the start of the test session.

    This fixture ensures that environment variables are available for all tests
    without requiring explicit calls to load them.

    Scope:
        session (runs once per test session)
    """
    load_dotenv()