from typing import List

from src.config.ExchangeConfig import ExchangeConfig
from src.connectors.ExchangeConnector import ExchangeConnector
from src.connectors.MEXCConnetor import MEXCConnector


class ConnectorFactory:

    @staticmethod
    def make_connector(name: str, exchanges_config: List[ExchangeConfig]) -> ExchangeConnector:
        exchange_config: ExchangeConfig = list(filter(lambda e: e.name.lower() == name.lower(), exchanges_config))[0]

        return {
            'mexc': MEXCConnector(exchange_config.api_key, exchange_config.api_secret)
        }[exchange_config.name.lower()]
