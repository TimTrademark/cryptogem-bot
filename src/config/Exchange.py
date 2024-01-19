from dataclasses import dataclass


@dataclass
class Exchange:

    def __init__(self, name: str, img: str, title: str, active: bool):
        self.name = name
        self.img = img
        self.title = title
        self.active = active
