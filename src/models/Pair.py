from src.models.Coin import Coin


class Pair:

    def __init__(self, coin0: Coin, coin1: Coin, tradable: bool):
        self.coin0 = coin0
        self.coin1 = coin1
        self.tradable = tradable

    def __str__(self):
        return f"{self.coin0.symbol}/{self.coin1.symbol}"
