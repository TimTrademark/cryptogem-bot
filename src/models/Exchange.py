class Exchange:

    def __init__(self, name: str, img: str, title: str, min_funds: float, active: bool):
        self.name = name
        self.img = img
        self.title = title
        self.min_funds = min_funds
        self.active = active
