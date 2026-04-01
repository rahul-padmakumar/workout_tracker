
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OperationalError
from django.core.management import call_command

from django.db.utils import OperationalError as DjangoOperationalError
from django.test import SimpleTestCase

class CommandTests(SimpleTestCase):
    """Tests for the wait_for_db management command."""

    @patch('core.management.commands.wait_for_db_command.Command.check')
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database when database is ready."""
        patched_check.return_value = True

        call_command('wait_for_db_command')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('core.management.commands.wait_for_db_command.Command.check')
    def test_wait_for_db_delayed(self, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OperationalError] * 2 + [DjangoOperationalError] * 3 + [True]
        
        call_command('wait_for_db_command')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])