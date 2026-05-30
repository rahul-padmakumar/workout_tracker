"""
Url patterns for the user API.
"""
from django.urls import path
from .views import (
    CreateUserView,
    CreateTokenView,
    ManageUserView,
    RefreshTokenView,
    OTPView,
    UserProfileImageUploadView,
    UserProfileAPIView,
    ResetPasswordView,
    ResetPasswordConfirmView,
)

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('login/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('otp/', OTPView.as_view(), name="otp"),
    path(
        'profile/image/upload/',
        UserProfileImageUploadView.as_view(),
        name='profile-image-upload',
    ),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path(
        'reset-password/',
        ResetPasswordView.as_view(),
        name='reset-password',
    ),
    path(
        'reset-password-confirm/',
        ResetPasswordConfirmView.as_view(),
        name='reset-password-confirm',
    ),
]
