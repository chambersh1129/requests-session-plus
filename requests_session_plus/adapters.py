"""requests_session_plus/adapters.py.

An enhanced HTTPAdapter that will set a timeout for all HTTP calls
"""
from requests.adapters import HTTPAdapter

DEFAULT_TIMEOUT: int = 5


class TimeoutAdapter(HTTPAdapter):
    """HTTP Adapter with a default timeout set to 5 seconds.

    Can overwrite the default timeout at initialization and when making calls

    Args:
        HTTPAdapter (HTTPAdapter): The built-in HTTP Adapter for urllib3
    """

    timeout: int = DEFAULT_TIMEOUT

    def __init__(self, *args, **kwargs):
        """Overwrite the timeout if provided as a parameter"""
        if "timeout" in kwargs:
            self.timeout = kwargs.pop("timeout")

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):  # pylint: disable=arguments-differ
        """Set the timeout at each HTTP call if it isn't provided.

        Args:
            request (Request): HTTP Request object

        Returns
            response: urllib3 Response object
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
