import math
import time
from typing import List

import ccxt
import requests

from src.connectors.ExchangeConnector import ExchangeConnector
from src.models.Coin import Coin
from src.models.Pair import Pair


class MEXCConnector(ExchangeConnector):

    def __init__(self, api_key: str = "", api_secret: str = ""):
        super().__init__(api_key, api_secret)
        if self.api_key == "" or self.api_secret == "":
            raise RuntimeError("MEXC: api key or api secret was empty, aborting...")
        self.mexc = ccxt.mexc({"apiKey": self.api_key, "secret": self.api_secret})

    def get_connector_name(self) -> str:
        return "MEXC"

    def execute_buy_order(self, pair: Pair, funds: float):
        self.mexc.create_market_buy_order_with_cost(
            self.get_formatted_pair_str(pair),
            funds
        )

    def get_latest_pairs(self) -> List[Pair]:
        current_timestamp = math.floor(time.time() * 1000)
        res = requests.get(
            f"https://www.mexc.com/api/operation/new_coin_calendar?timestamp={current_timestamp}"
        )
        json = res.json()
        pairs = self._convert_to_pairs(json)
        return pairs

    def _convert_to_pairs(self, json: str) -> List[Pair]:
        current_timestamp = math.floor(time.time() * 1000)
        return list(
            map(
                lambda p: Pair(
                    Coin(p["vcoinName"]),
                    Coin("USDT"),
                    current_timestamp >= p["firstOpenTime"],
                ),
                json["data"]["newCoins"],
            )
        )

    def get_formatted_pair_str(self, pair: Pair) -> str:
        return f"{pair.coin0.symbol}{pair.coin1.symbol}"
