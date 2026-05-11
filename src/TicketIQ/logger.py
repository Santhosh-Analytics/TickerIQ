from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from datetime import datetime


class LogSettings(BaseSettings):
    log_level: str = Field(default="INFO")
    log_max_byte: int = Field(default=5 * 1025 * 1024)
    log_backu_count: int = 5
    log_dir: str = Field(default="logs")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


class AppLogger(Exception):
    _configured: set[str] = set()

    def __init__(self, settings: LogSettings | None = None):
        self.settings = settings or LogSettings()
        self._setup_log_dir()

    def _setup_log_dir(self) -> None:
        self.log_dir = Path(self.settings.log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{datetime.now():%Y_%m_%d}.log"

    def _make_file_handler(self) -> RotatingFileHandler:
        handler = RotatingFileHandler(
            self.log_file,
            maxBytes=self.settings.log_max_byte,
            backupCount=self.settings.log_backu_count,
            encoding="utf-8",
        )
        fmt = logging.Formatter(
            "%(asctime)s || %(levelname)-8s || %(name)s || %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        handler.setLevel(self.settings.log_level)

        return handler

    def _make_console_handler(self) -> RichHandler:
        handler = RichHandler(
            markup=True, rich_tracebacks=True, show_time=True, show_path=True
        )
        handler.setLevel(getattr(logging, self.settings.log_level.upper()))
        return handler

    def get_logger(self, name: str) -> logging.Logger:
        logger = logging.Logger(name)
        if name in self._configured:
            return logger

        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._make_file_handler())
        logger.addHandler(self._make_console_handler())
        logger.propagate = False

        self._configured.add(name)
        return logger


_app_logger = AppLogger()


def get_logger(name: str) -> logging.Logger:
    return _app_logger.get_logger(name)


if __name__ == "__main__":
    log = get_logger(__name__)
    log = get_logger(__name__)
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")
