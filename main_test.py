"""Testing the app"""

from argparse import Namespace
import main
import os


class TestMain:
    """Testing the app"""

    def test_main(self):
        """Testing the app"""
        args = main.parse_args([
            '--host', 'localhost',
            '--port', '5432',
            '--username', 'test',
            '--password', 'azerty',
            '--database', 'test-db', '--reindex'])
        main.analyze_everything(args)
