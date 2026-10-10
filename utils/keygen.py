import random
import string
from datetime import datetime, timedelta

def generate_uuid_segment(length=5):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_key(prefix="mineminyee", tier="Free"):
    return f"{prefix}-uuid-{generate_uuid_segment()}"

def calculate_expiry(unit: str, amount: int):
    if unit == "Lifetime":
        return None  # None = 영구
    now = datetime.utcnow()
    if unit == "Hours":
        return now + timedelta(hours=amount)
    if unit == "Days":
        return now + timedelta(days=amount)
    return now + timedelta(hours=24)
