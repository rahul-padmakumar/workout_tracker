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
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken as Obtain
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from user.services.login_service import LoginService

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
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'email': user.email,
                'phone_number': user.phone_number
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            # pick the first field with an error
            error_key = next(iter(errors))

            # determine ui message code based on field and validation error
            ui_code = None
            if error_key == 'password':
                err = errors[error_key][0]
                if getattr(err, 'code', None) == 'min_length':
                    ui_code = 'password_too_short'
                else:
                    ui_code = 'password_not_strong_enough'
            elif error_key == 'phone_number':
                ui_code = 'invalid_phone_number'

            response_body = {'message': errors[error_key]}
            if ui_code is not None:
                response_body['ui_msg_code'] = ui_code

            return Response(response_body, status=status.HTTP_400_BAD_REQUEST)


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
            token, created = Token.objects.get_or_create(
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
        except InvalidCredentialsException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.INVALID_CREDENTIALS
                ),
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
        except Exception as e:
            print(f"Unexpected error during login: {type(e)}")
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
