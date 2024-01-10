from src.config.Config import Config
from src.connectors.ConnectorFactory import ConnectorFactory


def main():
    config = Config()
    connector = ConnectorFactory.make_connector('mexc', config.exchange_configs)
    pairs = connector.get_latest_pairs()
    for p in pairs:
        print(p)


if __name__ == '__main__':
    main()
