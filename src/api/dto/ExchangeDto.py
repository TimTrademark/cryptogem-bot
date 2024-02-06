class ExchangeDto:

    def __init__(self, name: str, img: str, title: str, funds: float, min_funds: float, active: bool):
        self.name = name
        self.img = img
        self.title = title
        self.funds = funds
        self.min_funds = min_funds
        self.active = active
