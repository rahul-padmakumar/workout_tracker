"""
Django management command to wait for the database to be ready.
"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Waits for the database to be ready before starting the application.'

    def handle(self, *args, **options):
        pass