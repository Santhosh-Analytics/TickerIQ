from pathlib import Path
from TicketIQ.config import Settings
from TicketIQ.config.main import get_settings

s = get_settings()

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = Path(s.paths.raw_data_dir) / "customer_support.csv"
print(f"File Path : {file_path}")

df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "thoughtvector/customer-support-on-twitter",
    "twcs/twcs.csv",
    # str(file_path),
)
print("First 5 records:", df.head())
