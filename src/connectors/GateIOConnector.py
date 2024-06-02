import json
import math
import time
from typing import List, Dict

import ccxt
import requests

from src.connectors.ExchangeConnector import ExchangeConnector
from src.models.Coin import Coin
from src.models.Pair import Pair


class GateIOConnector(ExchangeConnector):

    def __init__(self, api_key: str = "", api_secret: str = "", extra_args: Dict = {}):
        super().__init__(api_key, api_secret, extra_args)
        if self.api_key == "" or self.api_secret == "":
            raise RuntimeError("Gate.io: api key or api secret was empty, aborting...")
        self.gate = ccxt.gateio(
            {'apiKey': self.api_key, 'secret': self.api_secret})

    def get_connector_name(self) -> str:
        return "GateIO"

    def execute_buy_order(self, pair: Pair, funds: float):
        self.gate.create_market_buy_order_with_cost(self.get_formatted_pair_str(pair), funds)

    def get_balance(self, coin: Coin):
        balances = self.gate.fetch_balance()
        if len(balances["info"]) == 0:
            return 0
        else:
            for b in balances["info"]:
                if b["currency"].upper() == "USDT":
                    return b["available"]

    def get_latest_pairs(self) -> List[Pair]:
        res = requests.get("https://www.gate.io/price/view/new-cryptocurrencies", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})
        html = res.text
        new_pairs_json = json.loads(html.split("coinNew\":")[1].split(",\"coinGainers")[0])
        pairs = self._convert_to_pairs(new_pairs_json)
        return pairs

    def _convert_to_pairs(self, json: str) -> List[Pair]:
        current_timestamp = math.floor(time.time())
        return list(map(lambda p: Pair(Coin(p["symbol"]), Coin("USDT"), current_timestamp >= p["buy_start_timest"]),
                        json["list"]))

    def get_formatted_pair_str(self, pair: Pair) -> str:
        return f"{pair.coin0.symbol}_{pair.coin1.symbol}"
