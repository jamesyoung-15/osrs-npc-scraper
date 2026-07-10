from enum import Enum


class FetchFailureReason(Enum):
    """Enum for common fetch error message. Used to serialise failure reason to DB if needed."""

    NOT_FOUND = "not_found"
    RATE_LIMITED = "rate_limited"
    FORBIDDEN = "forbidden"
    REQUEST_TIMEOUT = "request_timeout"
    HTTPX_TIMEOUT = "httpx_timeout"
    BAD_REQUEST = "bad_request"
    UNKNOWN = "unknown"


class FetchError(Exception):
    """Custom exception for fetch errors"""

    def __init__(
        self,
        url: str,
        reason: FetchFailureReason,
        original_exception: Exception | None = None,
    ):
        self.url = url
        self.reason = reason
        self.original_exception = original_exception

        super().__init__(f"Failed to fetch {url}: {reason.value}")
