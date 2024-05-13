import abc
from typing import List

from src.models.Coin import Coin
from src.models.Pair import Pair


class ExchangeConnector:
    __metaclass__ = abc.ABCMeta

    def __init__(self, api_key: str = "", api_secret: str = "", extra_args=None):
        if extra_args is None:
            extra_args = {}
        self.api_key = api_key
        self.api_secret = api_secret
        self.extra_args = extra_args

    @abc.abstractmethod
    def get_connector_name(self) -> str:
        """Returns the connector name e.g. MEXC, Kucoin, ..."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_formatted_pair_str(self, pair: Pair) -> str:
        """Returns a formatted pair string e.g. BTC/USDT, BTC-USDT, ..."""
        raise NotImplementedError

    @abc.abstractmethod
    def execute_buy_order(self, pair: Pair, funds: float):
        """Buys a coin with given funds"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_balance(self, coin: Coin):
        """Gets balance of a coin"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_latest_pairs(self) -> List[Pair]:
        """Gets the latest pair list"""
        raise NotImplementedError
