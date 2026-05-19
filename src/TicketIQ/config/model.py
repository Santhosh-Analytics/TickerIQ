from enum import Enum
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class ModelName(str, Enum):
    """Supported pre-trained models for fine-tuning."""

    BERT = "bert-base-uncased"
    ROBERTA = "roberta-base"
    DISTILBERT = "distilbert-base-uncased"
    SENTIMENT = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    # MISTRAL = "mistralai/Mistral-7B-v0.1"


class TrainingParams(BaseModel):
    """Training hyperparameters - clean & reusable."""

    learning_rate: float = Field(default=2e-5, gt=0)
    per_device_train_batch_size: int = Field(default=16, gt=0)
    per_device_eval_batch_size: int = Field(default=32, gt=0)
    num_train_epochs: float = Field(default=3.0, gt=0)
    gradient_accumulation_steps: int = Field(default=2, gt=0)

    weight_decay: float = Field(default=0.01, ge=0)
    warmup_ratio: float = Field(default=0.1, ge=0, le=1.0)

    fp16: bool = True
    bf16: bool = False

    eval_steps: int = 100
    save_steps: int = 100
    logging_steps: int = 50

    load_best_model_at_end: bool = True
    metric_for_best_model: str = "f1"

    @model_validator(mode="after")
    def check_precision_flags(self) -> "TrainingParams":
        if self.fp16 and self.bf16:
            raise ValueError("fp16 and bf16 cannot both be True")
        return self


class HFTrainingSettings(BaseSettings):
    """Main Hugging Face Training Configuration."""

    model_config = SettingsConfigDict(extra="ignore")

    # Model Selection
    sentiment_model: ModelName = ModelName.SENTIMENT
    selected_model: ModelName = ModelName.BERT
    device_map: Literal["auto", "cpu", "cuda"] = "auto"
    training: TrainingParams = Field(default_factory=TrainingParams)
    num_labels: int = 2
    max_seq_length: int = 512

    # LoRA / PEFT
    use_lora: bool = True
    lora_r: int = Field(default=16, gt=0)
    lora_alpha: int = Field(default=32, gt=0)
    lora_dropout: float = Field(default=0.1, ge=0, le=1)


if __name__ == "__main__":
    model_config = HFTrainingSettings()
    print(model_config.model_dump())
