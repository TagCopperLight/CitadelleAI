from district import District
from role import Role


class GameState:
    def __init__(self, districts: list[District], roles: list[Role]) -> None:
        self.bank = 30
        self.districts = districts
        self.roles = roles

        self.current_player_id = 0
    
    def __repr__(self) -> str:
        return f"GameState(bank={self.bank}, districts={self.districts}, roles={self.roles}, current_player_id={self.current_player_id})"