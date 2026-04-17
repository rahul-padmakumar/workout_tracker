"""
Test cases for the User APIs.
"""

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """
    Helper function to create a user.
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the public features of the user API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': '1234567890'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.phone_number, payload['phone_number'])
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test creating a user that already exists fails.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': '1234567890'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password must be more than 5 characters.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'test@12',
            'phone_number': '1234567890'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_password_not_strong_enough(self):
        """
        Test that the password must be strong enough.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'password',
            'phone_number': '1234567890'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_phone_number_invalid(self):
        """
        Test that the phone number must be valid.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': 'invalid_phone_number'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_token_gen_for_valid_user(self):
        """
        Test that a token is generated for the valid user.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': '1234567890'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, {
            'email': payload['email'],
            'password': payload['password']
        })
        self.assertIn('token', res.data.get('data', None))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_gen_invalid_credentials(self):
        """
        Test that token is not generated if invalid credentials are given.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': '1234567890'
        }
        create_user(**payload)
        payload = {
            'email': 'test@example.com',
            'password': 'wrongpass@123'
        }
        res = self.client.post(TOKEN_URL, payload)
        print(res)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_gen_auth_error(self):
        """
        Test that token is not generated if invalid credentials are given.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': '1234567890'
        }
        create_user(**payload)
        payload = {
            'email': 'test1@example.com',
            'password': 'wrongpass@123'
        }
        res = self.client.post(TOKEN_URL, payload)
        print(res)
        self.assertIsNone(res.data.get('data', None))
        self.assertIsNotNone(res.data.get('errors', None))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_gen_empty_password(self):
        """
        Test that token is not generated if password is empty.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass@123',
            'phone_number': '1234567890'
        }
        create_user(**payload)
        print("Testing token generation with empty password")
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIsNone(res.data.get('data', None))
        self.assertIsNotNone(res.data.get('errors', None))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
