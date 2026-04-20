"""
Service for validating user passwords.
"""

import re
from user.exceptions import user_exceptions


def validate_password(password: str) -> bool:
    """Validate that the password is strong enough"""
    if len(password) < 8:
        raise user_exceptions.PasswordTooShortException(
            'Password must be at least 8 characters long'
        )
    pattern = r'(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9])'
    if not re.match(pattern, password):
        raise user_exceptions.PasswordNotStrongEnoughException(
            'Password must contain at least one letter, \
one number, and one special character'
        )
    return True
