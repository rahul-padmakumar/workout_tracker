"""
Url patterns for the user API.
"""

from django.urls import path
from .views import (
  CreateUserView,
  CreateTokenView
)

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('login/', CreateTokenView.as_view(), name='token'),
]
