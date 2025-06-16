from typing import Optional


class DiscordOAuth2Exception(Exception):
    """Base exception for Discord OAuth2 errors."""

    def __init__(
        self, message: str, *, original_exception: Optional[Exception] = None
    ) -> None:
        super().__init__(message)
        self.original_exception = original_exception


class DiscordAPIHTTPException(DiscordOAuth2Exception):
    """Exception for HTTP errors returned by Discord API."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        *,
        original_exception: Optional[Exception] = None,
    ) -> None:
        message = f"Discord API HTTP error {status_code}: {detail}"
        super().__init__(message, original_exception=original_exception)
        self.status_code = status_code
        self.detail = detail


class DiscordAPIValidationException(DiscordOAuth2Exception):
    """Exception for invalid data or unexpected response from Discord API."""

    def __init__(
        self, message: str, *, original_exception: Optional[Exception] = None
    ) -> None:
        super().__init__(message, original_exception=original_exception)
