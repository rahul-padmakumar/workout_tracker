from django.contrib import admin # noqa

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Define the admin page for users"""
    list_display = ['email', 'phone_number', 'is_active', 'is_staff']
    ordering = ['id']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('phone_number',)}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
