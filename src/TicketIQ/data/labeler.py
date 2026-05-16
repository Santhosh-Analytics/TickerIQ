from unicodedata import category
from .schema import CategoryLabel
import pandas as pd

category_keywords: dict[CategoryLabel, list[str]] = {
    CategoryLabel.BILLING: [
        "charged",
        "refund",
        "bill",
        "payment",
        "fees",
        "invoice",
        "price",
        "cost",
        "pay",
        "charge",
        "transaction",
        "receipt",
    ],
    CategoryLabel.SHIPPING: [
        "package",
        "deliver",
        "fedex",
        "ups",
        "courier",
        "shipping",
        "arrived",
        "tracking",
        "order",
        "sent",
    ],
    CategoryLabel.TECHNICAL: [
        "app",
        "error",
        "crash",
        "broken",
        "not working",
        "ios",
        "android",
        "update",
        "bug",
        "glitch",
        "website",
        "login",
        "password",
        "access",
    ],
    CategoryLabel.ACCOUNT: [
        "account",
        "email",
        "username",
        "profile",
        "sign in",
        "log in",
        "locked",
        "verify",
        "reset",
    ],
    CategoryLabel.SUBSCRIPTION: [
        "cancel",
        "subscription",
        "plan",
        "trial",
        "renew",
        "upgrade",
        "downgrade",
        "bundle",
        "premium",
    ],
}


def assign_category(text: str) -> CategoryLabel:
    counter = {category: 0 for category in category_keywords}
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text:
                counter[category] += 1
    best = max(counter, key=counter.get)
    if counter[best] == 0:
        return CategoryLabel.GENERAL
    return CategoryLabel(best.lower())
