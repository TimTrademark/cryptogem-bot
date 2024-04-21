import unittest

import ccxt.base.errors

from src.connectors.MEXCConnector import MEXCConnector


class MEXCIntegrationTests(unittest.TestCase):
    def test_get_latest_pairs(self):
        connector = MEXCConnector("test", "test")
        connector.mexc = ccxt.mexc()
        pairs = connector.get_latest_pairs()
        self.assertGreater(len(pairs), 0)
        self.assertGreater(len(pairs[0].coin0.symbol), 0)
        self.assertGreater(len(pairs[0].coin1.symbol), 0)


if __name__ == '__main__':
    unittest.main()
