"""
  tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class TestModels(TestCase):
    """Tests for models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = "testPass123"
        phone_number = "1234567890"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.phone_number, phone_number)