import logging
from typing import List, Callable

from src.config.Config import Config
from src.connectors.ConnectorFactory import ConnectorFactory
from src.connectors.ExchangeConnector import ExchangeConnector

logger = logging.getLogger("mycryptogem")


class ConfigLoader:

    def __init__(self):
        self.config = Config()
        self.connectors = self.get_connectors(self.config)
        self.add_callbacks = []

    def append_add_callback(self, callback: Callable):
        self.add_callbacks.append(callback)

    def on_add(self):
        for c in self.add_callbacks:
            c()

    def on_update(self):
        logger.info("Updating config")
        self.config = Config()
        self.connectors = self.get_connectors(self.config)

    def get_connectors(self, config: Config):
        connectors: List[ExchangeConnector] = []
        for e in config.exchange_configs:
            connectors.append(ConnectorFactory.make_connector(e.name, e.api_key, e.api_secret, e.extra_args))
        return connectors
