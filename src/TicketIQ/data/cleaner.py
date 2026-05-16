import random
from numpy import minimum
import pandas as pd
import re
import html
from TicketIQ.config import get_settings
from TicketIQ.logger import get_logger

MIN_WORD_COUNT = get_settings().data.min_word_count

dataset_sample_size = get_settings().data.dataset_sample_size
random_seed = get_settings().data.random_seed


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    filter_df = df[df["inbound"]].copy()
    filter_df = filter_df.drop(
        ["response_tweet_id", "in_response_to_tweet_id", "created_at", "author_id"],
        axis=1,
    )
    return filter_df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    ss = re.compile(r"@\w+")
    url = re.compile(r"http\S+|www\S+")
    get_logger(__name__).info(f"Sample text before: {df['text'].iloc[2]}")
    df["text"] = df["text"].apply(html.unescape)
    df["text"] = df["text"].str.replace(url, " ", regex=True)  # 1. URLs first
    df["text"] = df["text"].str.replace(ss, " ", regex=True)  # 2. mentions
    df["text"] = df["text"].str.lower()  # 3. lowercase
    df["text"] = (
        df["text"].str.replace(r"\s+", " ", regex=True).str.strip()
    )  # 4. collapse whitespace
    get_logger(__name__).info(f"Sample text after: {df['text'].iloc[2]}")
    before = len(df)
    df = df.drop_duplicates(subset=["text"]).copy()
    after = len(df)
    get_logger(__name__).info(f"Dedup removed {before - after} rows, {after} remaining")
    df = df[
        df["text"].str.encode("ascii", errors="ignore").str.len() / df["text"].str.len()
        > 0.8
    ].copy()

    before = len(df)
    df["word_count"] = df["text"].str.split().str.len()
    df = df[df["word_count"] >= MIN_WORD_COUNT].copy()
    df = df.drop(columns=["word_count"])
    df = df.sample(n=dataset_sample_size, random_state=random_seed).reset_index(
        drop=True
    )
    after = len(df)
    get_logger(__name__).info(
        f"Length filter removed {before - after} rows, {after} remaining"
    )
    print(df["text"].str.split().str.len().describe())
    return df
