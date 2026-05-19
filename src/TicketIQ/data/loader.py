from sys import exception
from TicketIQ.logger import get_logger
from TicketIQ.exception import DataLoadError
from TicketIQ.config.main import get_settings
import kagglehub
import pandas as pd
from pathlib import Path

settings = get_settings()
logger = get_logger(__name__)


def load_data() -> pd.DataFrame:
    data_dir = settings.paths.raw_data_dir
    KAGGLE_HANDLE = "thoughtvector/customer-support-on-twitter"
    try:
        if Path("/kaggle/input/").exists():
            csv_path = Path(
                "/kaggle/input/datasets/organizations/thoughtvector/customer-support-on-twitter/twcs/twcs.csv"
            )
            if not csv_path.exists():
                raise DataLoadError(
                    message="No twcs.csv found in Kaggle input",
                    error_code="DATA_LOAD_ERROR",
                )
        else:
            csv_path = Path(data_dir / "twcs/twcs.csv")
    except DataLoadError as e:
        print(f"Error: {e}, code={e.error_code}")

    try:
        if not csv_path.exists():
            logger.info(f"Downloading dataset to {data_dir}")
            kagglehub.dataset_download(
                handle=KAGGLE_HANDLE,
                output_dir=str(data_dir),
            )
        else:
            logger.info("Dataset already exists, skipping download")

        if not csv_path.exists():
            raise DataLoadError(
                message=f"File not found after download: {csv_path}",
                error_code="DATA_LOAD_ERROR",
            )

        logger.info(f"Reading data from {csv_path}")
        return pd.read_csv(csv_path)

    except DataLoadError:
        raise
    except Exception as e:
        logger.error("Data load failed", exc_info=True)
        raise DataLoadError(
            message=f"Failed to load dataset: {e}",
            error_code="DATA_LOAD_ERROR",
        ) from e


# def load_data() -> pd.DataFrame:
#     data_dir: Path = s.paths.raw_data_dir
#     Kaggle_path: str = None
#     get_logger(__name__).info(f"Downloading data from Kaggle to {s.paths.raw_data_dir}")
#     csv_path = data_dir / "twcs/twcs.csv"
#     try:
#         kagglehub.dataset_download(
#             handle="thoughtvector/customer-support-on-twitter",
#             # path=Kaggle_path,
#             output_dir=str(data_dir),
#         )
#         if not csv_path.exists():
#             raise DataLoadError(
#                 message=f"File not found after download: {csv_path}",
#                 error_code="DATA_LOAD_ERROR",
#             )
#         get_logger(__name__).info(f"Data has been read from {data_dir}")
#         return pd.read_csv(csv_path)
#
#     except Exception as e:
#         get_logger(__name__).error("Data load failed", exc_info=True)
#         raise DataLoadError(
#             message=f"File not found after download: {csv_path}",
#             error_code="DATA_LOAD_ERROR",
#         )
