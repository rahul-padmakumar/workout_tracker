import uuid
from django.db import models
from django.conf import settings
import os

def file_name(instance, filename):
        """Generate a unique filename for the uploaded user image"""
        ext = os.path.splitext(filename)[1]
        name= f"{uuid.uuid4()}{ext}"
        return f'user_images/{name}'

class UserProfile(models.Model):
    """Model to store additional information about the user"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    activity_level = models.CharField(max_length=20, null=True, blank=True)
    fitness_goals = models.TextField(null=True, blank=True)
    user_image = models.ImageField(upload_to=file_name, null=True, blank=True)

    def __str__(self):
        return f"{self.display_name}'s Profile"
