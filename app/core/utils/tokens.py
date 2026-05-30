from rest_framework_simplejwt.tokens import Token, AccessToken
from rest_framework_simplejwt.settings import api_settings


class PreAuthToken(Token):
    """Token used for pre-authentication steps, such as OTP verification."""
    token_type = 'pre_auth'
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['scope'] = ["otp:*"]


class FullAuthToken(AccessToken):
    """Token used for full authentication,
      providing access to all resources."""
    token_type = 'full_auth'
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['scope'] = ["api:*"]
