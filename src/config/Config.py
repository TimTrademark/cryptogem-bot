import json
from typing import List

from src.config.ExchangeConfig import ExchangeConfig


class Config:

    def __init__(self):
        self.exchange_configs: List[ExchangeConfig] = []
        with open("config.json") as f:
            content = f.read()
            json_config = json.loads(content)
            exchanges_dict = json_config["exchanges"]
            for e in exchanges_dict:
                self.exchange_configs.append(
                    ExchangeConfig(e, exchanges_dict[e]["api_key"], exchanges_dict[e]["api_secret"]))
