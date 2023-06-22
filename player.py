from district import District
from role import Role


class Player:
    def __init__(self) -> None:
        self.money: int
        self.role: Role

        self.hand: list[District]
        self.citadel: list[District]
        