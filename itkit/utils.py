"""
utils.py — Shared helpers for ITKit
"""

import secrets
import string
import datetime


def generate_password(length: int = 14) -> str:
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        # Ensure at least one of each required character type
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in "!@#$%^&*" for c in pwd)
        if has_upper and has_lower and has_digit and has_special:
            return pwd


def make_username(full_name: str) -> str:
    """Convert 'John Doe' → 'john.doe'"""
    parts = full_name.strip().lower().split()
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[-1]}"
    return parts[0]


def make_email(username: str, domain: str = "company.com") -> str:
    return f"{username}@{domain}"


def now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")
