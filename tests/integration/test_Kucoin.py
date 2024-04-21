import unittest

from src.connectors.KucoinConnector import KucoinConnector


class KucoinIntegrationTests(unittest.TestCase):
    def test_get_latest_pairs(self):
        connector = KucoinConnector("test", "test")
        pairs = connector.get_latest_pairs()
        self.assertGreater(len(pairs), 0)
        self.assertGreater(len(pairs[0].coin0.symbol), 0)
        self.assertGreater(len(pairs[0].coin1.symbol), 0)


if __name__ == '__main__':
    unittest.main()
