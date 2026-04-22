"""
User views for the user API.
"""
# Create your views here.

from core.utils.base_response import SuccessResponse, ErrorResponse
import core.utils.util as util
import core.utils.error_codes as error_codes
from user.exceptions.user_exceptions import (
  InvalidCredentialsException, UserLockoutException, UserNotRegisteredException
)

from rest_framework import generics, status, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken as Obtain
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from user.services.login_service import LoginService
from user.exceptions.user_exceptions import (
    PasswordNotStrongEnoughException,
    PasswordTooShortException,
    InvalidPhoneNumberException,
)
import user.services.validate_password_service as validate_password_service
import user.services.validate_phone_service as validate_phone_service

from .serializers import (
  UserSerializer,
  TokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Override create method to return custom response format"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            if validate_password_service.validate_password(
                serializer.validated_data['password']
            ) and validate_phone_service.validate_phone_number(
                serializer.validated_data['phone_number']
            ):
                user = serializer.save()
                response_data = {
                    'email': user.email,
                    'phone_number': user.phone_number
                }
                return SuccessResponse(
                    data=response_data
                )
        except PasswordNotStrongEnoughException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.PASSWORD_NOT_STRONG_ENOUGH,
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except PasswordTooShortException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.PASSWORD_TOO_SHORT,
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except InvalidPhoneNumberException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.INVALID_PHONE_NUMBER
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.VALIDATION_ERROR
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        # pylint: disable=broad-exception-caught
        except Exception as e:
            print(f"Unexpected error during user creation: {type(e)}")
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.SERVER_ERROR
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateTokenView(Obtain):
    """Create a new auth token for user"""
    serializer_class = TokenSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Override post method to return custom response format"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            login_service = LoginService()
            user = login_service.login_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                request=request
            )
            token, _ = Token.objects.get_or_create(
                user=user
            )
            return SuccessResponse(
                data={'token': token.key}
            )
        except UserNotRegisteredException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.USER_NOT_FOUND
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except InvalidCredentialsException as e:
            error_dict = util.ui_error(
                    error_codes.ErrorCodes.INVALID_CREDENTIALS
                )
            error_dict['attempt_count'] = e.attempt_count
            return ErrorResponse(
                errors=error_dict,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except UserLockoutException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.ACCOUNT_LOCKED
                ),
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except ValidationError:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.VALIDATION_ERROR
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        # pylint: disable=broad-exception-caught
        except Exception as e:
            print(f"Unexpected error during login: {type(e)}, {e}")
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.SERVER_ERROR
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
