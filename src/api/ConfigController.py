from typing import List

from flask import jsonify, Blueprint, request

from src.config.Exchange import Exchange
from src.config.ExchangeConfigManager import ExchangeConfigManager

manager = ExchangeConfigManager()

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/get-exchanges-configured', methods=["GET"])
def get_exchanges_configured():
    exchanges_configured: List[Exchange] = manager.get_exchanges_configured()
    return jsonify({"exchanges": _convert_exchanges_to_dict(exchanges_configured)})


@bp.route('/get-exchanges-not-configured', methods=["GET"])
def get_exchanges_not_configured():
    exchanges_not_configured: List[Exchange] = manager.get_exchanges_not_configured()
    return jsonify({"exchanges": _convert_exchanges_to_dict(exchanges_not_configured)})


@bp.route('/add-exchange-config', methods=["POST"])
def add_exchange_config():
    exchange_config_json = request.json
    try:
        manager.add_exchange_config(exchange_config_json["name"], exchange_config_json["api_key"],
                                    exchange_config_json["api_secret"])
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"success": "false"})


@bp.route('/delete-exchange-config', methods=["DELETE"])
def delete_exchange_config():
    exchange_config_json = request.json
    try:
        manager.delete_exchange_config(exchange_config_json["name"].lower())
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"success": "false"})


@bp.route('/toggle-active-exchange-config', methods=["POST"])
def toggle_active_exchange_config():
    exchange_config_json = request.json
    try:
        manager.toggle_active(exchange_config_json["name"].lower())
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"success": "false"})


def _convert_exchanges_to_dict(exchanges: List[Exchange]):
    return [{"name": e.name, "img": e.img, "title": e.title, "active": e.active} for e in exchanges]
