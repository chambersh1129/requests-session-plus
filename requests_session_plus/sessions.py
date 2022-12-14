from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3 import disable_warnings
from urllib3.util.retry import Retry

from .adapters import TimeoutAdapter
from .retries import SessionPlusRetry


class SessionPlus(Session):
    def __init__(
        self,
        retry: Retry = SessionPlusRetry(),
        adapter: HTTPAdapter = TimeoutAdapter(),
        raise_status_exceptions: bool = True,
        allow_insecure: bool = False,
    ):
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

    def _raise_exception_response_hook(self, response: Response, *args, **kwargs):
        """
        flake8 E731
        It is considered an anti-pattern to assign a lamba function to a variable.  It is best practice to have a
        function that returns the lamba function.
        """
        response.raise_for_status()
