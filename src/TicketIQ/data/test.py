from TicketIQ.data.keywords import category_keywords, priority_keywords
import re

category_patterns = {
    category: re.compile(
        "|".join(map(re.escape, keywords)),
        re.IGNORECASE,
    )
    for category, keywords in category_keywords.items()
}
print(category_patterns)
