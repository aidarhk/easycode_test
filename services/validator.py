from typing import Optional
from datetime import date
import re

def validate_date(birth_date_str: str) -> Optional[str]:
    match = re.match(r'^\s*(\d{1,2})\s*[./\-]\s*(\d{1,2})\s*$', birth_date_str.strip())
    if not match:
        return None
    
    day, month = int(match.group(1)), int(match.group(2))
    
    if not (1 <= day <= 31 and 1 <= month <= 12):
        return None
    
    try:
        normalized = date(date.today().year, month, day)
        return normalized.isoformat()
    except ValueError:
        return None
