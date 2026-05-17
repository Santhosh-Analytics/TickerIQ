from TicketIQ.data.schema import CategoryLabel, PriorityLabel, SentimentLabel
from TicketIQ.data.keywords import category_keywords, priority_keywords
import pandas as pd
import re
from TicketIQ.config import get_settings

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
    return best.value


def assign_priority(text: str) -> str:
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


from transformers import pipeline

SENTIMENT_MAP = {
    "LABEL_0": SentimentLabel.NEGATIVE.value,
    "LABEL_1": SentimentLabel.NEUTRAL.value,
    "LABEL_2": SentimentLabel.POSITIVE.value,
}

sentiment_pipeline = pipeline(
    "text-classification",
    model=settings.hf_training.sentiment_model,
    device=settings.hf_training.device_map.GPU,  # GPU on Kaggle
    truncation=True,
    max_length=128,
)


def assign_sentiment(text: str) -> str:
    if not isinstance(text, str) or not text.split():
        return SentimentLabel.NEUTRAL.value
    result = sentiment_pipeline(text)[0]
    return SENTIMENT_MAP.get(result["label"], SentimentLabel.NEUTRAL.value)


def applying_label(df: pd.DataFrame) -> pd.DataFrame:
    df["label"] = df["text"].apply(assign_category)
    df["priority"] = df["text"].apply(assign_priority)
    df.to_csv(str(labeled_csv), index=False)
    return df


def apply_sentiment_batch(df: pd.DataFrame) -> pd.DataFrame:
    texts = df["text"].tolist()
    results = sentiment_pipeline(texts, batch_size=64)
    df["sentiment"] = [
        SENTIMENT_MAP.get(r["label"], SentimentLabel.NEUTRAL.value) for r in results
    ]
    return df
