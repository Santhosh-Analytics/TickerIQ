from pathlib import Path
from TicketIQ.data import loader, cleaner

# from TicketIQ import exception
# from TicketIQ.logger import get_logger
# from TicketIQ.exception import DataLoadError
from TicketIQ.config.main import get_settings
from TicketIQ.data.schema import SentimentLabel
import pandas as pd
from TicketIQ.data.keywords import priority_keywords
from TicketIQ.data.labeler import assign_category, applying_label, apply_sentiment_batch
from TicketIQ.logger import get_logger
# pd.set_option("display.max_columns", 10)  # show all columns
# pd.set_option("display.width", 90)  # don’t wrap lines
# pd.set_option("display.max_colwidth", 90)  # show full text in each cell

pd.set_option("display.max_columns", None)  # show all columns
pd.set_option("display.width", None)  # don’t wrap lines
pd.set_option("display.max_colwidth", None)  # show full text in each cell

# import kagglehub
logger = get_logger(__name__)

settings = get_settings()
print(logger)


def get_cleaned_data():
    cleaned_csv = settings.paths.processed_data_dir / "cleaned_data.csv"
    labeled_csv = settings.paths.processed_data_dir / "labeled_data.csv"
    sentiment_csv = settings.paths.processed_data_dir / "sentiment_data.csv"

    if labeled_csv.exists():
        logger.info(f"Labeled data found at {labeled_csv}")
        df = pd.read_csv(labeled_csv)
        logger.info(f"Dataset rows: {len(df)}")
        df = apply_sentiment_batch(df)
        df.to_csv(sentiment_csv)
        logger.info("DF saved after sentiment labeled.")
        return df

    elif cleaned_csv.exists() and not labeled_csv.exists():
        logger.info(f"Cleaned data found at {cleaned_csv}")
        df = pd.read_csv(cleaned_csv)
        logger.info(f"Data length: {len(df)}")
        return applying_label(df)

    else:
        logger.info("No cleaned or processed data found. Running full pipeline.")
        df: pd.DataFrame = loader.load_data()
        df = cleaner.filter_data(df)
        df = cleaner.clean_data(df)
        logger.info(f"Final dataset rows: {len(df)}")
        return applying_label(df)


if __name__ == "__main__":
    df = get_cleaned_data()
    logger.info(f"Label Distribution: {df['label'].value_counts()}")
    logger.info(f"Priority Distribution: {df['priority'].value_counts()}")
