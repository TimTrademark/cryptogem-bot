import os
import unittest
from os.path import join, dirname

from dotenv import load_dotenv

from src.connectors.GateIOConnector import GateIOConnector
from src.models.Coin import Coin

dotenv_path = join(dirname(__file__), "../../.test.env")
load_dotenv(dotenv_path)


class GateIOIntegrationTests(unittest.TestCase):
    def test_get_latest_pairs(self):
        connector = GateIOConnector("test", "test")
        pairs = connector.get_latest_pairs()
        self.assertGreater(len(pairs), 0)
        self.assertGreater(len(pairs[0].coin0.symbol), 0)
        self.assertGreater(len(pairs[0].coin1.symbol), 0)

    def test_get_balance(self):
        connector = GateIOConnector(os.environ.get("GATEIO_TEST_API_KEY"), os.environ.get("GATEIO_TEST_API_SECRET"))
        self.assertGreaterEqual(connector.get_balance(Coin("USDT")), 0)


if __name__ == '__main__':
    unittest.main()
