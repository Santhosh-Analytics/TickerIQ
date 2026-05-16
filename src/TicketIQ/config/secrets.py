from pathlib import Path
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecretsSettings(BaseSettings):
    """Sensitive credentials and secrets."""

    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets" if Path("/run/secrets").exists() else None,
        extra="ignore",
    )

    hf_token: SecretStr | None = Field(
        default=None, description="Hugging Face Hub API token"
    )

    wandb_api_key: SecretStr | None = Field(
        default=None, description="Weights & Biases API key"
    )
