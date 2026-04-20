from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.db.models import Q, F
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
        if email and password:
            attempted_user = get_user_model().objects.filter(
                Q(email=email.lower())
            ).first()

            if not attempted_user:
                raise UserNotRegisteredException(
                    "User with this email does not exist"
                )

            user = authenticate(
                request=request,
                username=email,
                password=password
            )

            if not user:
                login_attempt_model = apps.get_model('core', 'LoginAttempt')

                with transaction.atomic():
                    manager = login_attempt_model.objects
                    login_attempt, _ = manager.get_or_create(
                        email=email.lower()
                    )

                    if login_attempt.attempt_count >= 2:
                        raise UserLockoutException(
                            "Account locked due to multiple failed\
login attempts. Please try again later.")

                    manager.filter(email=email.lower()).update(
                        attempt_count=F('attempt_count') + 1
                    )

                    raise InvalidCredentialsException("Invalid credentials")
            else:
                return user
