from pathlib import Path
import pydantic
from pydantic import Field, model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)

BASE_DIR = Path(__file__).absolute().resolve().parent
print(BASE_DIR)


class TikcetIQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file=str(BASE_DIR / "settings.toml"), case_sensitive=False, extra="ignore"
    )

    app_name: str = Field(default="TikcetIQ")
    debug: bool = Field(default=False)

    data_dir: Path = BASE_DIR / "data"
    log_dir: Path = Field(BASE_DIR / "logs")

    llm_model: str = Field(default="def")

    @model_validator(mode="after")
    def create_dir(self) -> TikcetIQSettings:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return super().settings_customise_sources(
            init_settings,
            env_settings,
            TomlConfigSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )


settings = TikcetIQSettings()

if __name__ == "__main__":
    print(settings.model_dump())
