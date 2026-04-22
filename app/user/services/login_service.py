"""
 Class for login use case
"""
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.db import transaction
from django.apps import apps
from user.exceptions.user_exceptions import (
    InvalidCredentialsException,
    UserLockoutException,
    UserNotRegisteredException
)


class LoginService:
    """Service for handling user login"""

    def login_user(self, email, password, request):
        """Login a user and return the user object if successful"""
        email_lower_case = email.lower() if email else None

        if not (email and password):
            raise InvalidCredentialsException(
                "Email and password are required"
            )

        attempted_user = get_user_model().objects.filter(
            email=email_lower_case
        ).first()

        if not attempted_user:
            raise UserNotRegisteredException(
                "User with this email does not exist"
            )

        try:
            account_lock_model = apps.get_model('core', 'AccountLock')
            account_lock, _ = account_lock_model.objects.get_or_create(
                email=email_lower_case
            )
        except LookupError:
            account_lock_model = None

        if account_lock.is_locked:
            if timezone.now() > account_lock.lock_until:
                account_lock.is_locked = False
                account_lock.save()
            else:
                raise UserLockoutException()

        user = authenticate(
            request=request,
            username=email_lower_case,
            password=password
        )

        # Try to get LoginAttempt model;
        # if missing, continue without recording attempts
        try:
            login_attempt_model = apps.get_model('core', 'LoginAttempt')
        except LookupError:
            login_attempt_model = None

        if not user:
            if login_attempt_model:
                with transaction.atomic():
                    login_attempt_model.objects.create(
                        email=email_lower_case,
                        successful=False
                    )

                account_lock.attempt_count += 1
                if account_lock.attempt_count >= 3:
                    account_lock.is_locked = True
                    account_lock.locked_at = timezone.now()
                    account_lock.locked_until = (
                        timezone.now() + timedelta(hours=24)
                    )
                    raise UserLockoutException(
                        "Account locked due to invalid"
                    )

                account_lock.save()
                raise InvalidCredentialsException(
                    count=account_lock.attempt_count
                )
        else:
            if login_attempt_model:
                login_attempt_model.objects.create(
                    email=email_lower_case,
                    successful=True
                )
            return user
