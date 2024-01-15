from typing import List

from src.models.Pair import Pair


class PairUtils:

    @staticmethod
    def filter_non_tradable_pairs(pair_list: List[Pair]):
        return list(filter(lambda p: not p.tradable, pair_list))

    @staticmethod
    def pair_exists_in_list(pair_list: List[Pair], pair: Pair) -> bool:
        for p in pair_list:
            if p.coin0.symbol == pair.coin0.symbol and p.coin1.symbol == pair.coin1.symbol:
                return True
        return False
