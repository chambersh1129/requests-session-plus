from requests.adapters import HTTPAdapter


class TimeoutAdapter(HTTPAdapter):
    """
    HTTP Adapter with a default timeout set to 2 seconds.

    Can overwrite the default timeout of 2 at initialization and when making calls

    Args:
        HTTPAdapter (HTTPAdapter): The built-in HTTP Adapter for urllib3
    """

    DEFAULT_TIMEOUT: int = 5

    def __init__(self, *args, **kwargs):
        self.timeout: int = self.DEFAULT_TIMEOUT

        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)
