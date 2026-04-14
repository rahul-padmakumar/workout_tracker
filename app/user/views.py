"""
User views for the user API.
"""
# Create your views here.

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer


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
            else:
                ui_code = 'invalid_input'

            return Response(
                {
                    'ui_msg_code': ui_code,
                    'message': errors[error_key]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
