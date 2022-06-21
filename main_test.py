"""Testing the app"""

import main


class TestMain:
    """Testing the app"""

    def test_main(self):
        """Testing the app"""
        args = main.parse_args([
            '--host', 'postgres',
            '--port', '5432',
            '--username', 'test',
            '--password', 'azerty',
            '--database', 'test-db', '--reindex'])
        main.analyze_everything(args)
