from district import District
from role import Role
from bank import Bank


class GameState:
    def __init__(self, districts: list[District], roles: list[Role]) -> None:
        self.bank = Bank()
        self.districts = districts
        self.roles = roles

        self.current_player_id = 0
    
    def __repr__(self) -> str:
        return f"GameState(bank={self.bank.value}, districts={len(self.districts)}, crown={self.current_player_id})"