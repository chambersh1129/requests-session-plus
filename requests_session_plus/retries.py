from urllib3.util.retry import Retry


class SessionPlusRetry(Retry):

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

        kwargs["backoff_factor"] = kwargs.get("backoff_factor", self.BACKOFF_FACTOR)
        kwargs["status_forcelist"] = kwargs.get("status_forcelist", self.STATUS_FORCELIST)
        kwargs["total"] = kwargs.get("total", self.TOTAL)

        super().__init__(*args, **kwargs)
