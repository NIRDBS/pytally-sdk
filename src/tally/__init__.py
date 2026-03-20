"""Unofficial Python SDK for the Tally.so API."""

from tally.client import TallyClient
from tally.constants import SUPPORTED_TALLY_API_VERSION
from tally.exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TallyAPIError,
    TallyConnectionError,
    TallyError,
    TallyTimeoutError,
    UnauthorizedError,
)

__version__ = "0.1.9"

# Alias for convenience
Tally = TallyClient

__all__ = [
    "BadRequestError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "SUPPORTED_TALLY_API_VERSION",
    "Tally",
    "TallyAPIError",
    "TallyClient",
    "TallyConnectionError",
    "TallyError",
    "TallyTimeoutError",
    "UnauthorizedError",
]
