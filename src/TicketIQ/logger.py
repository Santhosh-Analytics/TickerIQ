import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

from TicketIQ.config import Settings
from TicketIQ.config.main import get_settings


class AppLogger:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _make_file_handler(self) -> RotatingFileHandler:
        _handlers = RotatingFileHandler(
            filename=str(
                self.settings.paths.logs_dir / self.settings.logs.log_file_name
            ),
            maxBytes=self.settings.logs.log_max_bytes,
            backupCount=self.settings.logs.log_backup_count,
            encoding="utf-8",
        )
        fmt = logging.Formatter(self.settings.logs.log_fmt)
        _handlers.setFormatter(fmt)
        _handlers.setLevel(self.settings.logs.log_level)
        return _handlers

    def _make_console_handler(self) -> RichHandler:
        _handlers = RichHandler(
            level=self.settings.logs.log_level,
            show_level=True,
            show_time=True,
            markup=True,
            show_path=True,
            rich_tracebacks=True,
        )
        _handlers.setLevel(self.settings.logs.log_level)
        return _handlers

    def get_logger(self, name: str | None = None) -> logging.Logger:
        logger = logging.getLogger(name)
        if logger.handlers:
            return logger
        logger.setLevel(self.settings.logs.log_level)
        logger.propagate = False
        if self.settings.logs.log_to_console:
            logger.addHandler(self._make_console_handler())
        if self.settings.logs.log_to_file:
            logger.addHandler(self._make_file_handler())
        return logger


_app_logger = AppLogger(settings=get_settings())


def get_logger(name: str) -> logging.Logger:
    return _app_logger.get_logger(name)


if __name__ == "__main__":
    log = get_logger(__name__)
    print(log.name)
#     log = get_logger(__name__)
#     log.debug("debug message")
#     log.info("info message")
#     log.warning("warning message")
#     log.error("error message")
