"""
Service for validating user phone numbers.
"""

from user.exceptions import user_exceptions


def validate_phone_number(phone_number: str):
    """Validate that the phone number is valid"""
    if not phone_number.isdigit() or len(phone_number) != 10:
        raise user_exceptions.InvalidPhoneNumberException(
            'Phone number must be a 10-digit number'
        )
    return True
