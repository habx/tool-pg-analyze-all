"""Testing the app"""

import main
import os

class TestMain:
    """Testing the app"""

    def test_main(self):
        """Testing the app"""
        args = main.parse_args()
        args.database = os.getenv('PGDATABASE', 'test-db')
        args.user = os.getenv('PGUSER', 'test')
        args.password = os.getenv('PGPASSWORD', 'azerty')
        main.analyze_everything()
