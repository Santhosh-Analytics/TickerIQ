from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DockerSettings(BaseSettings):
    """Docker and runtime environment settings."""

    model_config = SettingsConfigDict(extra="ignore")

    environment: str = Field(
        default="development", pattern="^(development|staging|production)$"
    )

    use_gpu: bool = True
    num_workers: int = Field(default=4, gt=0)
    torch_dtype: str = Field(default="float16", pattern="^(float16|bfloat16|float32)$")

    # Resource limits
    max_memory_gb: float | None = None
    seed: int = 42

    # Whether to run in optimized mode (faster but less debugging)
    optimized_mode: bool = False
