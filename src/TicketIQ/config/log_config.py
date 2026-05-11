from datetime import datetime
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    log_level: str = Field(
        default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    log_max_bytes: int = Field(default=5 * 1024 * 1024)
    log_backup_count: int = 5
    log_to_console: bool = True
    log_to_file: bool = True
    log_file_name: str = f"{datetime.now():%Y_%m_%d}.log"
    log_fmt: str = "%(asctime)s || %(levelname)-8s || %(name)s || %(message)s"
    log_date: str = "%Y-%m-%d %H:%M:%S"

    # Experiment Tracking
    use_wandb: bool = False
    wandb_project: str | None = None
    wandb_entity: str | None = None
    wandb_log_model: bool = False

    use_tensorboard: bool = True
    use_mlflow: bool = False


if __name__ == "__main__":
    config = LogSettings()
    print(config.model_dump())
