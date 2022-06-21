"""Testing the app"""

import main

class TestMain:
    """Testing the app"""

    def test_main(self):
        """Testing the app"""
        args = main.parse_args()
        args.password = 'postgres'
        args.user = 'postgres'
        main.analyze_everything()
