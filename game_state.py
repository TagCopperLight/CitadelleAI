from district import District
from role import Role


class GameState:
    def __init__(self) -> None:
        self.bank = 30
        self.districts: list[District]
        self.roles: list[Role]

        self.current_player_id: int
    
    def is_over(self) -> bool:
        return False