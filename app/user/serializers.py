"""
User serializers for the user API.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models.user_profile import UserProfile
from drf_spectacular.utils import extend_schema_field


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        """Meta class for the serializer"""
        model = get_user_model()
        fields = ('email', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

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


# pylint: disable=abstract-method
class TokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for verifying user OTP"""
    otp = serializers.CharField(
        max_length=6
    )


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile object"""

    bmi = serializers.SerializerMethodField()
    user_image = serializers.ImageField(read_only=True)

    class Meta:
        """Meta class for the serializer"""
        model = UserProfile
        fields = [
            'display_name',
            'age',
            'weight',
            'height',
            'gender',
            'activity_level',
            'fitness_goals',
            'bmi',
            'user_image',
        ]

    @extend_schema_field(serializers.FloatField)
    def get_bmi(self, obj):
        """Calculate and return the BMI of the user"""
        if obj.height and obj.weight:
            height_in_m = obj.height / 100
            bmi = obj.weight / (height_in_m ** 2)
            return round(bmi, 2)
        return None


class UploadUserDpSerializer(serializers.ModelSerializer):
    """Serializer for uploading user display picture"""

    class Meta:
        """Meta class for the serializer"""
        model = UserProfile
        fields = ('user_image',)
        extra_kwargs = {'user_image': {'required': True}}


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for resetting user password"""
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset"""
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        min_length=8
    )
    email = serializers.EmailField()
    token = serializers.CharField()
