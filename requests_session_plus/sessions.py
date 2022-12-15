"""requests_session_plus/sessions.py.

Drop in replacement for requests.Session() object that enables:
    - Automatic retries with a backoff period between HTTP calls
    - Sets a timeout for every HTTP call
    - Raises exceptions when HTTP status code is >= 400
    - Can disable SSL certificate enforcement and disable warnings
"""
from typing import Optional

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import disable_warnings

from .adapters import TimeoutAdapter
from .retries import SessionPlusRetry


class SessionPlus(Session):
    """requests.Session() object with some quality of life enhancements."""

    def __init__(
        self,
        raise_status_exceptions: bool = False,
        retry: bool = True,
        timeout: Optional[int] = 5,
        verify: bool = True,
    ):
        """Instantiate SessionPlus object with retries and timeout enabled.

        Args:
            raise_status_exceptions (bool): Raise exceptions for status codes >=400. Defaults to False.
            retry (bool): Allow retries of failed HTTP calls. Defaults to True.
            timeout (int, None): Set a timeout for HTTP calls. Defaults to 5.
            verify (bool): Set verify=False to disable SSL verification and warnings. Defaults to True.

        """
        super().__init__()

        if not timeout:
            adapter = HTTPAdapter()

        else:
            adapter = TimeoutAdapter(timeout=timeout)

        if retry:
            adapter.max_retries = SessionPlusRetry()

        self.mount("https://", adapter)
        self.mount("http://", adapter)

        if raise_status_exceptions:
            self.hooks["response"].append(self._raise_exception_response_hook)

        if not verify:
            self.verify: bool = False
            disable_warnings()

    def _raise_exception_response_hook(self, response: Response, *args, **kwargs):  # pylint: disable=unused-argument
        """Set the post-response hook to raise an exception if HTTP status code is >=400.

        Args:
            response (Response): The object returned after HTTP call is made
        """
        response.raise_for_status()
