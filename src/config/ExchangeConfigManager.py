import json
from typing import Dict, List

from src.config.Exchange import Exchange


class ExchangeConfigManager:

    def __init__(self):
        self.exchanges: Dict[str, Dict[str]] = {}
        with open("exchanges.json", 'r') as f:
            content = f.read()
            json_config = json.loads(content)
            self.exchanges: Dict[str, Dict[str]] = json_config["exchanges"]

    def get_exchanges_configured(self):
        with open("config.json", 'r') as f:
            content = f.read()
            json_config = json.loads(content)
            exchanges_dict: Dict[str, Dict[str]] = json_config["exchanges"]
            exchanges_configured: List[Exchange] = list(
                map(lambda ex: Exchange(ex, self.exchanges[ex]["img"], self.exchanges[ex]["title"],
                                        exchanges_dict[ex]["active"]),
                    list(exchanges_dict.keys())))
        return exchanges_configured

    def get_exchanges_not_configured(self):
        exchanges_configured = self.get_exchanges_configured()
        exchanges_not_configured = []
        for e in list(self.exchanges.keys()):
            if e.lower() not in list(map(lambda ex: ex.name.lower(), exchanges_configured)):
                exchanges_not_configured.append(
                    Exchange(e, self.exchanges[e]["img"], self.exchanges[e]["title"], False))
        return exchanges_not_configured

    def add_exchange_config(self, name: str, api_key: str, api_secret: str):
        with open("config.json", 'r') as f:
            content = f.read()
        with open("config.json", 'w') as f:
            json_config = json.loads(content)
            json_config["exchanges"][name] = {"api_key": api_key,
                                              "api_secret": api_secret,
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
