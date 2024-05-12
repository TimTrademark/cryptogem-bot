from typing import List, Dict

import ccxt
import requests

from src.connectors.ExchangeConnector import ExchangeConnector
from src.models.Coin import Coin
from src.models.Pair import Pair


class KucoinConnector(ExchangeConnector):

    def __init__(self, api_key: str = "", api_secret: str = "", extra_args: Dict = {}):
        super().__init__(api_key, api_secret, extra_args)
        if self.api_key == "" or self.api_secret == "":
            raise RuntimeError("Kucoin: api key or api secret was empty, aborting...")
        self.kucoin = ccxt.kucoin(
            {'apiKey': self.api_key, 'secret': self.api_secret, 'password': self.extra_args["passphrase"]})

    def get_connector_name(self) -> str:
        return "Kucoin"

    def execute_buy_order(self, pair: Pair, funds: float):
        self.kucoin.create_order(self.get_formatted_pair_str(pair), "market", "buy", None, None, {
            "funds": funds,
        })

    def get_balance(self, coin: Coin):
        return float(self.kucoin.fetch_balance({"currency": coin.symbol})["info"]["data"][0]["available"])

    def get_latest_pairs(self) -> List[Pair]:
        res = requests.get("https://www.kucoin.com/_api/currency-front/v2/currency/latest?lang=en_US")
        json = res.json()
        pairs = self._convert_to_pairs(json)
        return pairs

    def _convert_to_pairs(self, json: str) -> List[Pair]:
        return list(
            map(lambda p: Pair(Coin(p["symbol"].split("-")[0], trade_precision=p["precision"]),
                               Coin(p["symbol"].split("-")[1]), p["tradeEnabled"]),
                json["data"]))

    def get_formatted_pair_str(self, pair: Pair) -> str:
        return f"{pair.coin0.symbol}-{pair.coin1.symbol}"
