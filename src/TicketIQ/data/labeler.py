from pydoc import text
from TicketIQ.data import keywords
from TicketIQ.data.schema import CategoryLabel, PriorityLabel
from TicketIQ.data.keywords import category_keywords, priority_keywords
import pandas as pd


def assign_category(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return CategoryLabel.GENERAL.value

    # main logic runs for all valid text
    counter = {category: 0 for category in category_keywords}
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text:
                counter[category] += 1

    best = max(counter, key=counter.get)
    if counter[best] == 0:
        return CategoryLabel.GENERAL.value
    return best.value


def assign_priority(text: str) -> str:
    if not isinstance(text, str) or not text.split():
        return PriorityLabel.LOW.value

    counter = {priority: 0 for priority in priority_keywords}
    for priority, keywords in priority_keywords.items():
        for keyword in keywords:
            if keyword in text:
                counter[priority] += 1
    best = max(counter, key=counter.get)
    if counter[best] == 0:
        return PriorityLabel.MEDIUM.value
    return best.value


def applying_label(df: pd.DataFrame) -> pd.DataFrame:
    df["label"] = df["text"].apply(assign_category)
    df["priority"] = df["text"].apply(assign_priority)
    return df
