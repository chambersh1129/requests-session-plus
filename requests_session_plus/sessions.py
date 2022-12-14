"""requests_session_plus/sessions.py.

Drop in replacement for requests.Session() object that enables:
    - Automatic retries with a backoff period between HTTP calls
    - Sets a timeout for every HTTP call
    - Raises exceptions when HTTP status code is >= 400
    - Can disable SSL certificate enforcement and disable warnings
"""

from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import disable_warnings
from urllib3.util.retry import Retry

from .adapters import TimeoutAdapter
from .retries import SessionPlusRetry


class SessionPlus(Session):
    """requests.Session() object with some quality of life enhancements.

    Args:
        Session (requests.Session): A Requests session
    """

    def __init__(
        self,
        retry: Retry = SessionPlusRetry(),
        adapter: HTTPAdapter = TimeoutAdapter(),
        raise_status_exceptions: bool = True,
        allow_insecure: bool = False,
    ):
        """Instantiate SessionPlus object will everything enabled except for allow_insecure.

        Args:
            retry (Retry, optional): Allow retries of failed HTTP calls. Defaults to SessionPlusRetry().
            adapter (HTTPAdapter, optional): Set a timeout for HTTP calls. Defaults to TimeoutAdapter().
            raise_status_exceptions (bool, optional): Raise exceptions for status codes >=400. Defaults to True.
            allow_insecure (bool, optional): Set verify=False and disable warnings. Defaults to False.
        """
        super().__init__()

        if not adapter:
            adapter = HTTPAdapter()

        if retry:
            adapter.max_retries = Retry.from_int(retry)

        self.mount("https://", adapter)
        self.mount("http://", adapter)

        if raise_status_exceptions:
            self.hooks["response"].append(self._raise_exception_response_hook)

        if allow_insecure:
            self.verify: bool = False
            disable_warnings()

    def _raise_exception_response_hook(self, response: Response, *args, **kwargs):  # pylint: disable=unused-argument
        """Set the post-response hook to raise an exception if HTTP status code is >=400.

        Args:
            response (Response): The object returned after HTTP call is made
        """
        response.raise_for_status()
