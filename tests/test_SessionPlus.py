"""tests/test_SessionPlus.py

All of the features we are using are already part of requests/urllib3 so we don't have to make external calls to
test every feature.  Instead we can just make sure classes and methods are updated as intended and trust that requests/
urllib3 are working as intended.
"""

import requests
import urllib3

from requests_session_plus.adapters import TimeoutAdapter
from requests_session_plus.retries import BACKOFF_FACTOR, STATUS_FORCELIST, TOTAL, SessionPlusRetry
from requests_session_plus.sessions import SessionPlus


def test_SessionPlus_defaults():
    session = SessionPlus()


def test_raise_status_exceptions():
    """Validate the response hook is configured correctly."""

    session = SessionPlus(
        retry=False,  # don't retry
        raise_status_exceptions=True,  # enable exceptions
        timeout=None,  # defaults to HTTPAdapter
        verify=True,  # verify certificate
    )

    assert "response" in session.hooks

    found_hook = False
    hook_name = SessionPlus._raise_exception_response_hook.__name__

    for hook in session.hooks["response"]:
        if hook.__name__ == hook_name:
            found_hook = True
            break

    assert found_hook


def test_retry_without_timeout():
    """Validate our SessionPlusRetry class gets applied correctly to the HTTPAdapter in the SessionPlus class."""

    session = SessionPlus(
        retry=True,  # ensure retries are enabled
        raise_status_exceptions=False,  # disable for first pass
        timeout=None,  # defaults to HTTPAdapter
        verify=True,  # verify certificate
    )

    protos = ["http://", "https://"]

    for proto in protos:
        assert proto in session.adapters
        assert session.adapters[proto].__class__ == requests.adapters.HTTPAdapter
        assert session.adapters[proto].max_retries.__class__ == SessionPlusRetry
        assert session.adapters[proto].max_retries.total == TOTAL
        assert session.adapters[proto].max_retries.backoff_factor == BACKOFF_FACTOR
        assert session.adapters[proto].max_retries.status_forcelist == STATUS_FORCELIST


def test_retry_with_timeout():
    """Validate our SessionPlusRetry class gets applied correctly to the TimeoutAdapter in the SessionPlus class."""

    session = SessionPlus(
        retry=True,  # ensure retries are enabled
        raise_status_exceptions=False,  # disable for first pass
        timeout=5,  # use the TimeoutAdapter
        verify=True,  # verify certificate
    )

    protos = ["http://", "https://"]

    for proto in protos:
        assert proto in session.adapters
        assert session.adapters[proto].__class__ == TimeoutAdapter
        assert session.adapters[proto].max_retries.__class__ == SessionPlusRetry
        assert session.adapters[proto].max_retries.total == TOTAL
        assert session.adapters[proto].max_retries.backoff_factor == BACKOFF_FACTOR
        assert session.adapters[proto].max_retries.status_forcelist == STATUS_FORCELIST


def test_timeout_without_retry():
    """Validate our TimeoutAdapter can be created with a default urllib3 Retry class."""
    session = SessionPlus(
        retry=False,  # don't retry
        raise_status_exceptions=False,  # disable for first pass
        timeout=5,  # use the TimeoutAdapter
        verify=True,  # verify certificate
    )

    protos = ["http://", "https://"]

    for proto in protos:
        assert proto in session.adapters
        assert session.adapters[proto].__class__ == TimeoutAdapter
        assert session.adapters[proto].max_retries.__class__ == urllib3.util.retry.Retry
        assert session.adapters[proto].max_retries.total == 0  # urllib3 Retry default
        assert session.adapters[proto].max_retries.backoff_factor == 0  # urllib3 Retry default


def test_with_allow_insecure():
    pass
