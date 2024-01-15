import json
from typing import List

from src.config.ExchangeConfig import ExchangeConfig


class Config:

    def __init__(self):
        self.exchange_configs: List[ExchangeConfig] = []
        self.funds = 0
        self.scheduling_timeout_seconds = 0
        with open("config.json") as f:
            content = f.read()
            json_config = json.loads(content)
            self.funds = json_config["funds"]
            self.scheduling_timeout_seconds = json_config["scheduling_timeout_seconds"]
            exchanges_dict = json_config["exchanges"]
            for e in exchanges_dict:
                self.exchange_configs.append(
                    ExchangeConfig(e, exchanges_dict[e]["api_key"], exchanges_dict[e]["api_secret"]))
