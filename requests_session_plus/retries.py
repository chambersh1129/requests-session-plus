"""requests_session_plus/retries.py.

An enhanced urllib3.util.retry.Retr() class which:
    - enables retries, 3 by default
    - sets a backoff factor to wait some amount of time between retrying HTTP calls
    - expands the list of HTTP status codes to retry

Not all HTTP status codes warrant a retry, which is why the STATUS_FORCELIST exists.  It will retry if any of these
status codes are returned.  Other 4xx or 5xx status codes may not be resolved with a retry so they are not listed.
"""
from urllib3.util.retry import Retry


class SessionPlusRetry(Retry):
    """Enhanced Retry with some helpful features enabled.

    Args:
        Retry (urllib3.util.retry.Retry): Base urllib3 Retry definition
    """

    BACKOFF_FACTOR: float = 2.5

    STATUS_FORCELIST: list[int] = [
        413,  # Client: Payload Too Large
        429,  # Client: Too Many Requests
        500,  # Server: Internal Server Error
        502,  # Server: Bad Gateway
        503,  # Server: Service Unavailable
        504,  # Server: Gateway Timeout
    ]

    TOTAL: int = 3

    def __init__(self, *args, **kwargs):
        """All of these settings are supported in the default Retry object, so just update the kwargs and pass it on."""
        kwargs["backoff_factor"] = kwargs.get("backoff_factor", self.BACKOFF_FACTOR)
        kwargs["status_forcelist"] = kwargs.get("status_forcelist", self.STATUS_FORCELIST)
        kwargs["total"] = kwargs.get("total", self.TOTAL)

        super().__init__(*args, **kwargs)
