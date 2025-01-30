import re

from core.constants import PATTERNS


def validate_password(password: str) -> str:
    try:
        if not re.match(pattern=PATTERNS["PASSWORD"], string=password):
            raise ValueError(
                "Password must contain at least 1 digit, 1 lowercase, 1 uppercase, 1 special character, and be between 8-64 characters long."
            )

        return password

    except Exception as error:
        raise error
