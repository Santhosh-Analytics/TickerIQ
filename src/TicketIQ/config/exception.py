from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


class ErrorResponse(BaseModel):
    """Standard error response model."""

    success: bool = False
    error_code: str
    message: str
    details: dict[str, Any] | None = None


class ExceptionSettings(BaseSettings):
    """Exception handling and error reporting settings."""

    model_config = SettingsConfigDict(extra="ignore")

    # Error handling behavior
    debug_mode: bool = False  # Show full traceback in development
    raise_on_validation_error: bool = True

    # Logging
    log_exceptions: bool = True
    include_traceback_in_logs: bool = True

    # Custom exception messages
    default_error_message: str = "An unexpected error occurred"

    # Sentry / Error tracking (optional)
    use_sentry: bool = False
    sentry_dsn: SecretStr | None = None

    # Whether to exit on critical errors
    exit_on_critical_error: bool = True
