from TicketIQ.config.main import get_settings
from TicketIQ.config import ExceptionSettings
import sys
import traceback


class TicketIQException(Exception):
    _settings: ExceptionSettings = get_settings().exception

    def __init__(
        self, message: str | None = None, error_code: str = "TICKETIQ_ERROR", tb=None
    ) -> None:
        self.message = message or self._settings.default_error_message
        self.error_code = error_code
        self.traceback_info = (
            self._extract(tb) if self._settings.include_traceback_in_logs else None
        )
        super().__init__(self.message)

    def _extract(self, tb) -> str | None:
        if tb is None:
            return None
        extracted = traceback.extract_tb(tb)
        if not extracted:
            return None
        frame = extracted[-1]
        return f"{frame.filename}, line {frame.lineno}, in {frame.name}"

    def __str__(self) -> str:
        if self.traceback_info and self._settings.debug_mode:
            # return f"[P2PRAGException] {self.message}\n  → {self.traceback_info}"
            return f" {self.message}\n  → {self.traceback_info}"
        # return f"[P2PRAGException] {self.message}"
        return f" {self.message}"


class DataException(TicketIQException):
    pass


class DataLoadError(DataException):
    pass


if __name__ == "__main__":
    try:
        x = 1 / 0  # trigger a real exception
    except Exception:
        ex = TicketIQException(
            message="Something went wrong",
            error_code="DIVIDE_ERROR",
            tb=sys.exc_info()[2],  # ✓ valid inside except block
        )
        print(ex)
