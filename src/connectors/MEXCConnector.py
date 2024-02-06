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
        self.mexc = ccxt.mexc({'apiKey': self.api_key, 'secret': self.api_secret})

    def get_connector_name(self) -> str:
        return "MEXC"

    def execute_buy_order(self, pair: Pair, funds: float):
        self.mexc.create_order(self.get_formatted_pair_str(pair), "market", "buy", None, None, {
            "quoteOrderQty": funds,
        })

    def get_latest_pairs(self) -> List[Pair]:
        res = requests.get("https://www.mexc.com/api/platform/spot/market-v2/web/coin/new/list")
        json = res.json()
        pairs = self._convert_to_pairs(json)
        for p in pairs:
            ticker = self.mexc.fetch_ticker(self.get_formatted_pair_str(p))
            if ticker["info"]["openTime"] != "0":
                p.tradable = True
        return pairs

    def _convert_to_pairs(self, json: str) -> List[Pair]:
        return list(map(lambda p: Pair(Coin(p["cn"]), Coin(p["mn"]), False), json["data"]))

    def get_formatted_pair_str(self, pair: Pair) -> str:
        return f"{pair.coin0.symbol}{pair.coin1.symbol}"
