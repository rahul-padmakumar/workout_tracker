from django.contrib import admin # noqa

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Define the admin page for users"""
    list_display = ['email', 'phone_number', 'is_active', 'is_staff']
    ordering = ['id']


