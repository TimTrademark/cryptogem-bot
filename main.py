import time
from typing import List, Dict

from flask import Flask
from flask_cors import CORS

from src.api import ConfigController
from src.api.ControlPanelController import ControlPanelController
from src.config.Config import Config
from src.connectors.ConnectorFactory import ConnectorFactory
from src.connectors.ExchangeConnector import ExchangeConnector
from src.models.ExchangeConfig import ExchangeConfig
from src.models.Pair import Pair
from src.utils.PairUtils import PairUtils

app = Flask(__name__, template_folder='control_panel', static_url_path='',
            static_folder='control_panel/static', )
app.add_url_rule('/', view_func=ControlPanelController.index, methods=["GET"])
app.register_blueprint(ConfigController.bp)
CORS(app)


def main():
    app.run()
    config = Config()
    connectors: List[ExchangeConnector] = get_connectors(config)
    last_non_tradable: Dict[str, List[Pair]] = init_last_non_tradable(connectors)
    while True:
        for connector in connectors:
            ec: ExchangeConfig = config.get_exchange_config_by_name(connector.get_connector_name())
            if not ec.active:
                continue
            latest_pairs = connector.get_latest_pairs()
            compare_latest_pairs_and_trade(connector, latest_pairs, ec.funds,
                                           last_non_tradable[connector.get_connector_name().lower()])
            last_non_tradable[connector.get_connector_name().lower()] = PairUtils.filter_non_tradable_pairs(
                latest_pairs)
        time.sleep(config.scheduling_timeout_seconds)


def get_connectors(config: Config):
    connectors: List[ExchangeConnector] = []
    for e in config.exchange_configs:
        connectors.append(ConnectorFactory.make_connector(e.name, e.api_key, e.api_secret))
    return connectors


def init_last_non_tradable(connectors: List[ExchangeConnector]):
    last_non_tradable: Dict[str, List[Pair]] = {}
    for c in connectors:
        last_non_tradable[c.get_connector_name().lower()] = PairUtils.filter_non_tradable_pairs(c.get_latest_pairs())
    return last_non_tradable


def compare_latest_pairs_and_trade(connector: ExchangeConnector, latest_pairs: List[Pair], funds: float,
                                   last_non_tradable: List[Pair]):
    print("Latest pairs:")
    print(list(map(lambda lp: str(lp), latest_pairs)))
    for p in latest_pairs:
        if p.tradable and PairUtils.pair_exists_in_list(last_non_tradable, p):
            print(f"{str(p)} has opened trading, buying coin...")
            buy(p, funds, connector)


def buy(pair: Pair, funds: float, connector: ExchangeConnector):
    connector.execute_buy_order(pair, funds)


if __name__ == '__main__':
    main()
