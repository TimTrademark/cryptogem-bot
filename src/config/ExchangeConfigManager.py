import json
from typing import Dict, List

from src.api.dto.ExchangeDto import ExchangeDto
from src.exceptions.IllegalFundsAmountException import IllegalFundsAmountException


class ExchangeConfigManager:

    def __init__(self):
        self.exchanges: Dict[str, Dict[str]] = {}
        with open("exchanges.json", 'r') as f:
            content = f.read()
            json_config = json.loads(content)
            self.exchanges: Dict[str, Dict[str]] = json_config["exchanges"]

    def get_exchanges_configured(self) -> List[ExchangeDto]:
        with open("config.json", 'r') as f:
            content = f.read()
            json_config = json.loads(content)
            exchanges_dict: Dict[str, Dict[str]] = json_config["exchanges"]
            exchanges_configured: List[ExchangeDto] = list(
                map(lambda ex: ExchangeDto(ex, self.exchanges[ex]["img"], self.exchanges[ex]["title"],
                                           exchanges_dict[ex]["funds"], self.exchanges[ex]["min_funds"],
                                           exchanges_dict[ex]["active"]),
                    list(exchanges_dict.keys())))
        return exchanges_configured

    def get_exchanges_not_configured(self) -> List[ExchangeDto]:
        exchanges_configured = self.get_exchanges_configured()
        exchanges_not_configured = []
        for e in list(self.exchanges.keys()):
            if e.lower() not in list(map(lambda ex: ex.name.lower(), exchanges_configured)):
                exchanges_not_configured.append(
                    ExchangeDto(e, self.exchanges[e]["img"], self.exchanges[e]["title"], 0,
                                self.exchanges[e]["min_funds"], False))
        return exchanges_not_configured

    def add_exchange_config(self, name: str, api_key: str, api_secret: str, funds: float):
        with open("config.json", 'r') as f:
            content = f.read()
            json_config = json.loads(content)
            min_funds: float = self.exchanges[name]["min_funds"]
            if funds < min_funds:
                raise IllegalFundsAmountException(
                    f"Funds amount is too low for {name}, minimum amount is {min_funds} USDT")
        with open("config.json", 'w') as f:
            json_config["exchanges"][name] = {"api_key": api_key,
                                              "api_secret": api_secret,
                                              "funds": funds,
                                              "active": True}
            f.write(json.dumps(json_config))

    def delete_exchange_config(self, name: str):
        with open("config.json", 'r') as f:
            content = f.read()
        with open("config.json", 'w') as f:
            json_config = json.loads(content)
            del json_config["exchanges"][name]
            f.write(json.dumps(json_config))

    def toggle_active(self, name: str):
        with open("config.json", 'r') as f:
            content = f.read()
        with open("config.json", 'w') as f:
            json_config = json.loads(content)
            json_config["exchanges"][name]["active"] = not json_config["exchanges"][name]["active"]
            f.write(json.dumps(json_config))
