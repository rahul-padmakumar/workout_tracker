import pyotp
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from user.exceptions import user_exceptions


def generate_secret() -> str:
    """Generate secret for user otp"""
    return pyotp.random_base32()


def fetch_otp(user) -> str:
    """helper for fetching and saving otp info"""
    otp_model = apps.get_model('core', 'OTP')
    saved_otp_info, created = otp_model.objects.get_or_create(user=user)
    print(otp_model.objects.first().user)
    if created or not saved_otp_info.secret:
        print("Generating secret")
        secret = generate_secret()
        saved_otp_info.secret = secret
    else:
        print(f"Hi all {saved_otp_info}")
        secret = saved_otp_info.secret
    otp = pyotp.TOTP(secret, interval=180).now()
    saved_otp_info.user = user
    saved_otp_info.generated_at = timezone.now()
    saved_otp_info.otp_code = otp
    saved_otp_info.expires_at = timezone.now() + timedelta(minutes=3)
    saved_otp_info.is_used = False
    saved_otp_info.save()
    return otp


def verify_otp(user, otp) -> bool:
    """helper for verifying otp"""
    otp_model = apps.get_model('core', 'OTP')
    saved_otp_info, created = otp_model.objects.get_or_create(user=user)

    if created or not saved_otp_info.otp_code:
        raise user_exceptions.OTPNotRequestedException

    account_lock = apps.get_model('core', 'AccountLock')
    user_entry_in_lock, _ = account_lock.objects.get_or_create(
        email=user.email
    )

    if user_entry_in_lock and user_entry_in_lock.is_locked:
        raise user_exceptions.UserLockoutException

    secret = saved_otp_info.secret
    totp = pyotp.TOTP(secret, interval=180)
    if totp.verify(otp, valid_window=0):

        if saved_otp_info.is_used:
            raise user_exceptions.OTPReuseException

        saved_otp_info.is_used = True
        saved_otp_info.save()
        user_entry_in_lock.is_locked = False
        user_entry_in_lock.attempt_count = 0
        user_entry_in_lock.save()
        return True, 0
    else:
        user_entry_in_lock.attempt_count += 1
        if user_entry_in_lock.attempt_count >= 3:
            user_entry_in_lock.is_locked = True
            user_entry_in_lock.locked_at = timezone.now()
            user_entry_in_lock.locked_until = (
                timezone.now() + timedelta(hours=24)
            )
            raise user_exceptions.UserLockoutException(
                "Account locked due to invalid"
            )
        user_entry_in_lock.save()
        return False, user_entry_in_lock.attempt_count
