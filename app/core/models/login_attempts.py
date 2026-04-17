from django.db import models


class LoginAttempt(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    attempt_count = models.IntegerField(default=0)

    def __str__(self):
        return f"LoginAttempt(\
email={self.email}, successful={self.successful},\
timestamp={self.timestamp}, attempt_count={self.attempt_count})"
