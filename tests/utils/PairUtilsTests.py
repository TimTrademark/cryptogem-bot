import unittest

from src.models.Coin import Coin
from src.models.Pair import Pair
from src.utils.PairUtils import PairUtils


class PairUtilsTests(unittest.TestCase):
    def test_filter_non_tradable_pairs_should_not_contain_tradable_pairs(self):
        c1 = Coin("p1")
        c2 = Coin("p2")
        p1 = Pair(c1, c1, False)
        p2 = Pair(c2, c2, True)
        pairs = [p1, p1, p2]
        filtered = PairUtils.filter_non_tradable_pairs(pairs)
        self.assertEqual(len(filtered), 2)

    def test_pair_should_exist_in_list(self):
        c1 = Coin("x")
        c2 = Coin("y")
        p1 = Pair(c1, c2, True)
        pairs = [p1]
        exists = PairUtils.pair_exists_in_list(pairs, p1)
        self.assertEqual(exists, True)

    def test_pair_should_not_exist_in_list(self):
        c1 = Coin("x")
        c2 = Coin("y")
        p1 = Pair(c1, c2, True)
        p2 = Pair(c1, c1, True)
        pairs = [p1]
        exists = PairUtils.pair_exists_in_list(pairs, p2)
        self.assertEqual(exists, False)


if __name__ == '__main__':
    unittest.main()
