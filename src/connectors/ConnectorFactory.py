from src.connectors.ExchangeConnector import ExchangeConnector
from src.connectors.MEXCConnector import MEXCConnector


class ConnectorFactory:

    @staticmethod
    def make_connector(name: str, api_key: str, api_secret: str) -> ExchangeConnector:
        return {
            'mexc': MEXCConnector(api_key, api_secret)
        }[name.lower()]
