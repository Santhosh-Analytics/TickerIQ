from ast import main
from pathlib import Path
from pydoc import importfile
from pydantic import Field, model_validator
from pydantic_core.core_schema import AfterValidatorFunctionSchema
from pydantic_settings import BaseSettings, SettingsConfigDict


class PathsSettings(BaseSettings):
    """doc string"""

    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[3])

    data_dir: Path | None = Field(default=None)
    raw_data_dir: Path | None = Field(default=None)
    processed_data_dir: Path | None = Field(default=None)
    splits_data_dir: Path | None = Field(default=None)

    logs_dir: Path | None = Field(default=None)
    output_dir: Path | None = Field(None)
    hf_cache_dir: Path | None = Field(default=None)

    artifacts_dir: Path | None = Field(default=None)
    model_dir: Path | None = Field(default=None)
    metrics_dir: Path | None = Field(default=None)

    @model_validator(mode="after")
    def finalize_and_create_paths(self) -> "PathsSettings":
        main_folders: dict = {
            "data_dir": "data",
            "logs_dir": "logs",
            "output_dir": "outputs",
            "hf_cache_dir": "hf_cache",
            "artifacts_dir": "artifacts",
        }
        for attr, name in main_folders.items():
            if getattr(self, attr) is None:
                setattr(self, attr, self.base_dir / name)
            getattr(self, attr).mkdir(parents=True, exist_ok=True)
        sub_folders: dict = {
            "raw_data_dir": self.data_dir / "raw",
            "processed_data_dir": self.data_dir / "processed",
            "splits_data_dir": self.data_dir / "splits",
            "model_dir": self.artifacts_dir / "models",
            "metrics_dir": self.artifacts_dir / "metrics",
        }

        for attr, name in sub_folders.items():
            if getattr(self, attr) is None:
                setattr(self, attr, name)
            getattr(self, attr).mkdir(parents=True, exist_ok=True)
        return self


paths = PathsSettings()


if __name__ == "__main__":
    print(paths.model_dump())
