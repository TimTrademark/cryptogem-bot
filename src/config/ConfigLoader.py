from typing import List

from src.config.Config import Config
from src.connectors.ConnectorFactory import ConnectorFactory
from src.connectors.ExchangeConnector import ExchangeConnector


class ConfigLoader:

    def __init__(self):
        self.config = Config()
        self.connectors = self.get_connectors(self.config)

    def update(self):
        print("Updating config")
        self.config = Config()
        self.connectors = self.get_connectors(self.config)

    def get_connectors(self, config: Config):
        connectors: List[ExchangeConnector] = []
        for e in config.exchange_configs:
            connectors.append(ConnectorFactory.make_connector(e.name, e.api_key, e.api_secret))
        return connectors
