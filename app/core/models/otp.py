from django.db import models
from django.conf import settings


class OTP(models.Model):
    """ User otp model"""

    user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="user"
    )

    otp_code = models.CharField(max_length=6, blank=True, null=True)
    generated_at = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(null=True)
    is_used = models.BooleanField(default=False)
    secret = models.CharField(max_length=255)
