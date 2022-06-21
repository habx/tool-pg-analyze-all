"""Testing the app"""
import os

import main


class TestMain:
    """Testing the app"""

    def test_main(self):
        """Testing the app"""
        args = main.parse_args([
            '--host', os.getenv('PGHOST', 'postgres'),  # For CircleCI
            '--port', '5432',
            '--username', 'test',
            '--password', 'azerty',
            '--database', 'test-db',
            # '--reindex',  # <-- Completely hangs the test
        ])
        main.analyze_everything(args)
