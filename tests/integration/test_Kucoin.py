import os
import unittest
from os.path import join, dirname

from dotenv import load_dotenv

from src.connectors.KucoinConnector import KucoinConnector
from src.models.Coin import Coin

dotenv_path = join(dirname(__file__), "../../.test.env")
load_dotenv(dotenv_path)


class KucoinIntegrationTests(unittest.TestCase):
    def test_get_latest_pairs(self):
        connector = KucoinConnector("test", "test", extra_args={"passphrase": ""})
        pairs = connector.get_latest_pairs()
        self.assertGreater(len(pairs), 0)
        self.assertGreater(len(pairs[0].coin0.symbol), 0)
        self.assertGreater(len(pairs[0].coin1.symbol), 0)

    def test_get_balance(self):
        connector = KucoinConnector(os.environ.get("KUCOIN_TEST_API_KEY"), os.environ.get("KUCOIN_TEST_API_SECRET"),
                                    extra_args={"passphrase": os.environ.get("KUCOIN_TEST_PASSWORD")})
        self.assertGreaterEqual(connector.get_balance(Coin("USDT")), 0)


if __name__ == '__main__':
    unittest.main()
