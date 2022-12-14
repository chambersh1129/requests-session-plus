"""requests_session_plus/adapters.py.

An enhanced HTTPAdapter that will set a timeout for all HTTP calls
"""
from requests.adapters import HTTPAdapter


class TimeoutAdapter(HTTPAdapter):
    """HTTP Adapter with a default timeout set to 2 seconds.

    Can overwrite the default timeout of 2 at initialization and when making calls

    Args:
        HTTPAdapter (HTTPAdapter): The built-in HTTP Adapter for urllib3
    """

    DEFAULT_TIMEOUT: int = 5

    def __init__(self, *args, **kwargs):
        """Allow the overriding of the DEFAULT_TIMEOUT and set it if it wasn't provided."""
        self.timeout = self.DEFAULT_TIMEOUT

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):  # pylint: disable=arguments-differ
        """Set the timeout at each HTTP call if it isn't provided.

        Args:
            request (Request): HTTP Request object

        Returns
            response: requests Response object
        """
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
