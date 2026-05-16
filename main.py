from pathlib import Path

from TicketIQ.data import loader, cleaner

# from TicketIQ import exception
# from TicketIQ.logger import get_logger
# from TicketIQ.exception import DataLoadError
from TicketIQ.config.main import get_settings
import pandas as pd
from TicketIQ.data.keywords import priority_keywords
from TicketIQ.data.labeler import assign_category, applying_label
from TicketIQ.logger import get_logger

# pd.set_option("display.max_columns", 10)  # show all columns
# pd.set_option("display.width", 90)  # don’t wrap lines
# pd.set_option("display.max_colwidth", 90)  # show full text in each cell

pd.set_option("display.max_columns", None)  # show all columns
pd.set_option("display.width", None)  # don’t wrap lines
pd.set_option("display.max_colwidth", None)  # show full text in each cell

# import kagglehub


def get_cleaned_data():
    cleaned_csv: Path = get_settings().paths.processed_data_dir / "cleaned_data.csv"
    if cleaned_csv.exists():
        get_logger(__name__).info(f"Cleaned data found at {cleaned_csv}, reading it.")
        df = pd.read_csv(cleaned_csv)
        get_logger(__name__).info(f"Data length: {df.count()}")
        return applying_label(df)
    else:
        get_logger(__name__).info("No cleaned data found, processing from raw...")
        df: pd.DataFrame = loader.load_data()
        df = cleaner.filter_data(df)
        df = cleaner.clean_data(df)
        get_logger(__name__).info(f"Data length: {len(df)}")
        return applying_label(df)


if __name__ == "__main__":
    df = get_cleaned_data()
    get_logger(__name__).info(f"Label Distribution: {df['label'].value_counts()}")
    get_logger(__name__).info(f"Priority Distribution: {df['priority'].value_counts()}")
    critical_samples = df[df["priority"] == "critical"]["text"].sample(
        20, random_state=42
    )
    print(critical_samples.to_string())
