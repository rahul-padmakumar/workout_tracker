"""
Unit tests for the calc module.
"""
from django.test import SimpleTestCase
from .calc import add


class CalcTest(SimpleTestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
