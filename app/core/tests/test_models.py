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

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test@EXAMPLE.com', 'test@example.com'],
            ['TEST1@EXAMPLE.COM', 'TEST1@example.com'],
            ['test2@EXAMPLE.COM', 'test2@example.com'],
            ['test3@EXAMPLE.COM', 'test3@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123', '1234567890')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123', '1234567890')
