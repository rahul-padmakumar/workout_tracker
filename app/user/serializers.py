"""
User serializers for the user API.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
import re


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
                'Password must contain at least \
                  one letter, one number, and one special character'
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
