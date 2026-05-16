from pydantic import BaseModel
from enum import Enum


class CategoryLabel(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    SHIPPING = "shipping"
    ACCOUNT = "account"
    SUBSCRIPTION = "subscription"
    GENERAL = "general"


class PriorityLabel(str, Enum):
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TicketLabel(BaseModel):
    category: CategoryLabel
    priority: PriorityLabel
    sentiment: SentimentLabel


class RawTicket(BaseModel):
    id: str
    text: str
    label: TicketLabel | None = None
