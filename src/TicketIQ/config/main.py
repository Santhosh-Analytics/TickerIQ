# ----------------(*)----------------(*)----------------(*)-----------------#
# _BaseSettings: The core class from pydantic-settings that adds settings loading from multiple sources (environment variables, secret files, TOML files, etc.).
#
# PydanticBaseSettingsSource: An abstract base class for all settings sources.
# SettingsConfigDict: A typed dictionary for configuration of the Settings class (e.g., specifying the TOML file path).

# TomlConfigSettingsSource: A concrete source that loads settings from a TOML file.
# ----------------(*)----------------(*)-----------------(*)-----------------# model_config is a special attribute that configures the whole model.
# BaseSettings load values from env vars, dotenv, TOML, YAML, secrets, init arguments

# toml_file tells BaseSettings to also load settings from the TOML file at that path.
# classmethod - This is a factory hook provided by pydantic-settings. Because the configuration of sources must be defined before any instance is created, it is a class method. It allows you to change the default loading behaviour (e.g., drop .env files, add TOML support) without modifying the library’s internals. The method receives the class (cls) and the default sources, and returns the customised order. This is a class method that customises the order and set of sources from which settings are loaded.

# model_config where we define source settings file path.

# settings_customise_sources - It tells pydantic which sources be used and in what order (order in the function return)

# TomlConfigSettingsSource(settings_cls) - Internally, it reads model_config.toml_file, parses toml, converts to dict. Matches keys to model fields and validates type.
# How does the code “read” settings, When you call Settings()? - The class calls settings_customise_sources to obtain the list of sources (init, env, TOML). Load each source – Each source produces a dictionary of key‑value pairs. Merge – Sources are merged in the order returned (init has highest priority, then env, then TOML). Validate – Pydantic checks that each field’s value matches the declared type and any additional constraints. Instantiate – The final validated dictionary is used to create the Settings object.
# ----------------(*)----------------(*)-----------------(*)-----------------#


from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = Field(default="TicketIQ")
    debug: bool = Field(default=False)

    data_dir: Path = Field(default=BASE_DIR / "data")
    log_dir: Path = Field(default=BASE_DIR / "logs")

    llm_model: str = Field(default="default")
    llm_base_url: str = Field(default="default")

    model_config = SettingsConfigDict(
        toml_file=str(BASE_DIR / "settings.toml"),
        case_sensitive=False,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
        )


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
