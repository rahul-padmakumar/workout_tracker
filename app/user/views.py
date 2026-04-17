"""
User views for the user API.
"""
# Create your views here.

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken as Obtain
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import (
  UserSerializer,
  TokenSerializer
)
from core.utils.base_response import SuccessResponse, ErrorResponse
import core.utils.util as util


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
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return SuccessResponse(
                data={'token': token.key},
                message='Authentication successful.'
            )
        else:
            error = util.get_custom_error(serializer.errors)
            error_response = util.flatten_errors(serializer.errors)
            if error == 'invalid_credentials':
                return ErrorResponse(
                    errors=error_response,
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return ErrorResponse(
                    errors=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
