from typing import Dict

from src.connectors.ExchangeConnector import ExchangeConnector
from src.connectors.KucoinConnector import KucoinConnector
from src.connectors.MEXCConnector import MEXCConnector


class ConnectorFactory:

    @staticmethod
    def make_connector(name: str, api_key: str, api_secret: str, extra_args: Dict) -> ExchangeConnector:
        lower_name = name.lower()
        if lower_name == 'mexc':
            return MEXCConnector(api_key, api_secret, extra_args)
        elif lower_name == 'kucoin':
            return KucoinConnector(api_key, api_secret, extra_args)
