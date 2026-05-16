from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    min_word_count: int = Field(default=8, gt=0)
    min_ascii_ratio: float = Field(default=0.8, gt=0, le=1.0)
    dataset_sample_size: int | None = Field(default=None)  # None = use all
    random_seed: int = 42


if __name__ == "__main__":
    ds = DataSettings()
    ds.model_dump()
