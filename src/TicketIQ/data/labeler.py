from TicketIQ.data.schema import CategoryLabel, PriorityLabel, SentimentLabel
from TicketIQ.data.keywords import category_keywords, priority_keywords
import pandas as pd
import re
from TicketIQ.config import get_settings
from TicketIQ.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()
category_patterns = {
    category: re.compile(
        "|".join(map(re.escape, keywords)),
        re.IGNORECASE,
    )
    for category, keywords in category_keywords.items()
}

priority_patterns = {
    priority: {
        re.compile(re.escape(keyword), re.IGNORECASE): weight
        for keyword, weight in keywords.items()
    }
    for priority, keywords in priority_keywords.items()
}

labeled_csv = settings.paths.processed_data_dir / "labeled_data.csv"
from transformers import pipeline
import torch


def assign_category(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return CategoryLabel.GENERAL.value

    # main logic runs for all valid text
    counter = {category: 0 for category in category_keywords}
    for category, pattern in category_patterns.items():
        counter[category] = len(pattern.findall(text))

    best = max(counter, key=counter.get)
    if counter[best] == 0:
        return CategoryLabel.GENERAL.value
    logger.info("Category labeling completed")
    return best.value


def assign_priority(text: str) -> str:
    logger.info("Started assigning priority")
    if not isinstance(text, str) or not text.split():
        return PriorityLabel.MEDIUM.value

    counter = {priority: 0 for priority in priority_keywords}
    for priority, patterns in priority_patterns.items():
        for pattern, weight in patterns.items():
            matches = len(pattern.findall(text))
            counter[priority] += matches * weight
    best = max(counter, key=counter.get)
    if counter[best] == 0:
        return PriorityLabel.MEDIUM.value
    return best.value


# def assign_sentiment(text: str) -> str:
#     if not isinstance(text, str) or not text.split():
#         return SentimentLabel.NEUTRAL.value
#     result = sentiment_pipeline(text)[0]
#     return SENTIMENT_MAP.get(result["label"], SentimentLabel.NEUTRAL.value)


def applying_label(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Started category and priority labeling")
    df["label"] = df["text"].apply(assign_category)
    df["priority"] = df["text"].apply(assign_priority)
    logger.info("Category and Priority labeling completed.")
    df.to_csv(str(labeled_csv), index=False)
    logger.info(f"Saving labeled data frame to {labeled_csv}.")
    return df


SENTIMENT_MAP = {
    "LABEL_0": SentimentLabel.NEGATIVE.value,
    "LABEL_1": SentimentLabel.NEUTRAL.value,
    "LABEL_2": SentimentLabel.POSITIVE.value,
}

sentiment_pipeline = pipeline(
    "text-classification",
    model=settings.hf_training.sentiment_model.value,
    device=0 if torch.cuda.is_available() else -1,
    truncation=True,
    max_length=128,
)


def apply_sentiment_batch(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(
        f"Started mapping sentiment using {settings.hf_training.sentiment_model.value} model"
    )
    texts = df["text"].tolist()
    results = sentiment_pipeline(texts, batch_size=64)
    df["sentiment"] = [
        SENTIMENT_MAP.get(r["label"], SentimentLabel.NEUTRAL.value) for r in results
    ]

    logger.info("Setiment mapping completed")

    return df
