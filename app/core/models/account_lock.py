"""
Model class for Account Lock
"""

from django.db import models


class AccountLock(models.Model):

    """
    Model class for Account lock
    """

    class LockoutReason(models.TextChoices):
        """
        Model class for LockoutReason
        """
        WRONG_PASSWORD = 'wrong_password', 'WRONG_PASSWORD'
        WRONG_OTP = 'wrong_otp', 'WRONG_OTP'

    email = models.EmailField(max_length=255, null=False, unique=True)
    attempt_count = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True)
    locked_until = models.DateTimeField(null=True)
    lockout_reason = models.CharField(
        max_length=100,
        choices=LockoutReason.choices
    )
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
