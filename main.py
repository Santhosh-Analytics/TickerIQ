from TicketIQ.data import loader, cleaner

# from TicketIQ import exception
# from TicketIQ.logger import get_logger
# from TicketIQ.exception import DataLoadError
from TicketIQ.config.main import get_settings
import pandas as pd

# import kagglehub
#
s = get_settings()
df: pd.DataFrame = loader.load_data()
df = cleaner.filter_data(df)
df = cleaner.clean_data(df)
print(df["text"].sample(20, random_state=42).to_string())
print(f"Data lenght: {df.count()}")


from TicketIQ.data.labeler import assign_category

for i in df["text"]:
    ss = assign_category(i)
    print(i)
    print(ss)
    break
