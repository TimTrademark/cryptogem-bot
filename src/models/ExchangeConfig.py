from typing import Dict


class ExchangeConfig:

    def __init__(self, name: str, api_key: str, api_secret: str, funds: float, active: bool, extra_args: Dict):
        self.name = name
        self.api_key = api_key
        self.api_secret = api_secret
        self.funds = funds
        self.active = active
        self.extra_args = extra_args
