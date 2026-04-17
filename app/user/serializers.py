"""
User serializers for the user API.
"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
import re
from django.db.models import Q
import core.utils.util as util
import core.utils.error_codes as error_codes
from django.apps import apps


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def validate_password(self, value):
        """Validate that the password is strong enough"""
        if len(value) < 8:
            raise serializers.ValidationError(
                'Password must be at least 8 characters long'
                )
        pattern = r'(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9])'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Password must contain at least one letter, \
one number, and one special character'
            )
        return value

    def validate_phone_number(self, value):
        """Validate that the phone number is valid"""
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Phone number must be entered in the format: \
+999999999. Up to 15 digits allowed.'
            )
        return value

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


# pylint disable=abstract-method
class TokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """ Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            attempted_user = get_user_model().objects.filter(
                Q(email=email.lower())
            ).first()

            if not attempted_user:
                raise serializers.ValidationError(
                    util.ui_error(
                        "User not found",
                        error_codes.ErrorCodes.USER_NOT_FOUND
                    ),
                    code=error_codes.ErrorCodes.USER_NOT_FOUND
                )

            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                login_attempt_model = apps.get_model('core', 'LoginAttempt')
                manager = login_attempt_model.objects
                login_attempt, created = manager.get_or_create(
                    email=email.lower()
                )

                if login_attempt.attempt_count >= 2:
                    error_response = util.ui_error(
                            "Account locked due to \
multiple failed login attempts. Please try again later.",
                            error_codes.ErrorCodes.ACCOUNT_LOCKED
                        )
                    error_response["is_locked"] = True
                    raise serializers.ValidationError(
                        error_response,
                        code=error_codes.ErrorCodes.ACCOUNT_LOCKED
                    )

                login_attempt.attempt_count += 1
                login_attempt.save()

                raise serializers.ValidationError(
                    util.ui_error(
                        "Invalid credentials",
                        error_codes.ErrorCodes.INVALID_CREDENTIALS
                    ),
                    code=error_codes.ErrorCodes.INVALID_CREDENTIALS
                )
            attrs['user'] = user
            return attrs
