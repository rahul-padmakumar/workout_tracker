"""
User views for the user API.
"""
# Create your views here.

import os
from dotenv import load_dotenv
from core.models.user import User
from core.utils.base_response import SuccessResponse, ErrorResponse
import core.utils.util as util
import core.utils.error_codes as error_codes
from user.exceptions.user_exceptions import (
    InvalidCredentialsException,
    UserLockoutException,
    UserNotRegisteredException,
    OTPNotRequestedException,
    OTPReuseException,
)

from rest_framework import generics, status, mixins
from core.utils.custom_authentication import (
  CustomAuthentication as JWTAuthentication
)
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from user.services.login_service import LoginService
from user.exceptions.user_exceptions import (
    PasswordNotStrongEnoughException,
    PasswordTooShortException,
    InvalidPhoneNumberException,
)
import user.services.validate_password_service as validate_password_service
import user.services.validate_phone_service as validate_phone_service
import user.services.otp_service as otp_service

from .serializers import (
  UploadUserDpSerializer,
  UserProfileSerializer,
  UserSerializer,
  TokenSerializer,
  VerifyOTPSerializer,
  ResetPasswordSerializer,
  ResetPasswordConfirmSerializer
)

from django.utils import timezone

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from drf_spectacular.utils import extend_schema

from django.utils.translation import gettext as _
from rest_framework.views import APIView
from django.apps import apps

from core.utils.tokens import PreAuthToken
from core.utils.permissions import IsPreAuthToken, IsFullAuthToken
from core.tasks import send_email
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


load_dotenv()


# Load environment variables from .env file
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


class CreateTokenView(TokenObtainPairView):
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
            token = PreAuthToken()
            token["user_id"] = str(user.id)

            return SuccessResponse(
                data={
                    'token': str(token)
                }
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFullAuthToken]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class RefreshTokenView(TokenRefreshView):
    """View for token refresh"""
    @extend_schema(
        summary="Refresh JWT token",
        description="Takes refresh token and returns new access token"
    )
    def post(self, request, *args, **kwargs):
        try:
            res = super().post(request, *args, **kwargs)
            return SuccessResponse(
                    data=res.data
                )
        except InvalidToken:
            return ErrorResponse(
                errors=util.ui_error(
                    message=_('Token not accepted'),
                    ui_msg_code=error_codes.ErrorCodes.INVALID_TOKEN
                )
            )
        # pylint: disable=broad-exception-caught
        except Exception as e:
            return ErrorResponse(
                errors=util.ui_error(
                    message=e,
                    ui_msg_code=error_codes.ErrorCodes.SERVER_ERROR
                )
            )


class OTPView(APIView):
    """
    View for otp fetch and verification
    """
    serializer_class = VerifyOTPSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPreAuthToken]

    def get(self, request):
        """ Generate and return otp"""
        otp_value = otp_service.fetch_otp(request.user)
        send_email.delay(
            subject="Your OTP Code",
            message=f"Your OTP code is: {otp_value}",
            sender_email=os.environ.get("EMAIL_HOST_USER"),
            recipient_email=request.user.email
        )
        return SuccessResponse(
            data={
                "otp": str(otp_value)
            }
        )

    def post(self, request):
        """Verify generated OTP"""
        otp_value = request.data.get("otp")

        try:
            is_verified, count = otp_service.verify_otp(
                request.user, otp_value
            )
            if is_verified:
                token = RefreshToken.for_user(request.user)

                access = token.access_token
                access["type"] = "full_auth"
                access["scope"] = ["api:*"]

                refresh = token
                refresh["type"] = "full_auth"
                refresh["scope"] = ["api:*"]

                return SuccessResponse(
                    data={
                        "refresh": str(refresh),
                        "access": str(access)
                    }
                )
            else:
                return ErrorResponse(
                    errors={
                        'message': 'Not valid otp',
                        'attempt_count': count
                    }
                )
        except OTPNotRequestedException:
            return ErrorResponse(
                errors=util.ui_error(
                    message=_("OTP not requested"),
                    ui_msg_code=error_codes.ErrorCodes.OTP_NOT_REQUESTED
                )
            )
        except OTPReuseException:
            return ErrorResponse(
                errors=util.ui_error(
                    message=_("OTP reused"),
                    ui_msg_code=error_codes.ErrorCodes.OTP_REUSED
                )
            )
        except UserLockoutException:
            return ErrorResponse(
                errors=util.ui_error(
                    message=_("User lockout"),
                    ui_msg_code=error_codes.ErrorCodes.ACCOUNT_LOCKED
                )
            )


class UserProfileAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    """
    View for user profile management
    """
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFullAuthToken]

    queryset = apps.get_model('core', 'UserProfile').objects.all()

    def get_object(self):
        """Retrieve and return user profile"""
        UserProfileModel = apps.get_model('core', 'UserProfile')
        profile, _ = UserProfileModel.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def patch(self, request, *args, **kwargs):
        """Update user profile"""
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Retrieve user profile"""
        return self.retrieve(request, *args, **kwargs)


class UserProfileImageUploadView(
        mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    View for uploading user profile image
    """
    serializer_class = UploadUserDpSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFullAuthToken]

    def get_object(self):
        """Retrieve and return user profile"""
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        """Update user profile image"""
        return self.partial_update(request, *args, **kwargs)


class ResetPasswordView(APIView):
    """
    View for sending password reset email
    """
    serializer_class = ResetPasswordSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """Send password reset email"""
        try:
            email = request.data.get("email")
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = None
        except MultipleObjectsReturned:
            user = None
        if user:
            encoded_email = urlsafe_base64_encode(force_bytes(user.email))
            token = default_token_generator.make_token(user)
            reset_link = (
                f"{os.environ.get('FRONTEND_URL')}/reset-password-confirm/"
                f"{encoded_email}.{token}"
            )
            send_email.delay(
                subject=_("Password Reset"),
                message=_(
                    f"Click the link to reset your password: {reset_link}"
                ),
                sender_email=os.environ.get("EMAIL_HOST_USER"),
                recipient_email=user.email,
            )

        return SuccessResponse(
            data={
                "message": _(
                    "If an account with that email exists, a password "
                    "reset link has been sent."
                )
            }
        )


class ResetPasswordConfirmView(APIView):
    """
    View for confirming password reset and setting new password
    """
    serializer_class = ResetPasswordConfirmSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """Validate token and set new password"""
        try:
            email = request.data.get("email")
            token = request.data.get("token")
            user = User.objects.get(email=email)
        except (
            TypeError,
            ValueError,
            OverflowError,
            ObjectDoesNotExist,
            MultipleObjectsReturned
        ):
            user = None

        if user is None:
            return ErrorResponse(
                errors=util.ui_error(
                    message=_("Operation not allowed"),
                    ui_msg_code=error_codes.ErrorCodes.OPERATION_NOT_ALLOWED
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not default_token_generator.check_token(user, token):
            return ErrorResponse(
                errors=util.ui_error(
                    message=_("Invalid or expired password reset link"),
                    ui_msg_code=error_codes.ErrorCodes.INVALID_TOKEN
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            new_password = serializer.validated_data['new_password']
            if validate_password_service.validate_password(new_password):
                user.password_reset_on = timezone.now()
                user.set_password(new_password)
                user.save()
                return SuccessResponse(
                    data={
                        "message": _(
                            "Password has been reset successfully."
                            " Please login with your new password."
                        )
                    }
                )
        except PasswordNotStrongEnoughException:
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.PASSWORD_NOT_STRONG_ENOUGH,
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except (PasswordTooShortException, ValidationError):
            return ErrorResponse(
                errors=util.ui_error(
                    error_codes.ErrorCodes.PASSWORD_TOO_SHORT,
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
