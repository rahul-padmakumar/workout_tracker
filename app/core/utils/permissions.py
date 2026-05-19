from rest_framework.permissions import BasePermission

class IsPreAuthToken(BasePermission):
    """
    Custom permission to check if the token is a PreAuthToken.
    This can be used to restrict access to certain views until the user has completed pre-authentication steps.
    """

    def has_permission(self, request, view):
        # Check if the token is a PreAuthToken
        token = getattr(request, 'auth', None)
        return token is not None and getattr(token, 'token_type', None) == 'pre_auth'


class IsFullAuthToken(BasePermission):
    """
    Custom permission to check if the token is a FullAuthToken.
    This can be used to restrict access to certain views until the user has completed full authentication steps.
    """

    def has_permission(self, request, view):
        # Check if the token is a FullAuthToken
        token = getattr(request, 'auth', None)
        return token is not None and getattr(token, 'token_type', None) == 'full_auth'