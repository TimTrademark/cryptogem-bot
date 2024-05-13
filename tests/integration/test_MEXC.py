import os
import unittest
from os.path import join, dirname

import ccxt.base.errors
from dotenv import load_dotenv

from src.connectors.MEXCConnector import MEXCConnector
from src.models.Coin import Coin

dotenv_path = join(dirname(__file__), "../../.test.env")
load_dotenv(dotenv_path)


class MEXCIntegrationTests(unittest.TestCase):
    def test_get_latest_pairs(self):
        connector = MEXCConnector("test", "test")
        connector.mexc = ccxt.mexc()
        pairs = connector.get_latest_pairs()
        self.assertGreater(len(pairs), 0)
        self.assertGreater(len(pairs[0].coin0.symbol), 0)
        self.assertGreater(len(pairs[0].coin1.symbol), 0)

    def test_get_balance(self):
        connector = MEXCConnector(os.environ.get("MEXC_TEST_API_KEY"), os.environ.get("MEXC_TEST_API_SECRET"))
        self.assertGreaterEqual(connector.get_balance(Coin("USDT")), 0)


if __name__ == '__main__':
    unittest.main()
