from game_state import GameState
from district import District
from role import Role


class Player:
    def __init__(self, id: int) -> None:
        self.id = id

        self.money = 0
        self.role: Role = Role(0, "None")

        self.hand: list[District] = []
        self.citadel: list[District] = []
    
    def select_character(self, game_state: GameState, available_characters: list[Role], unavailable_characters: list[Role]) -> Role:
        return available_characters[0]
    
    def choose_money_district(self, game_state: GameState) -> bool:
        return True

    def build_district(self, game_state: GameState) -> None:
        pass

    def action(self, game_state: GameState) -> None:
        pass

    def __repr__(self) -> str:
        return f"Player(id={self.id}, money={self.money}, role={self.role}, hand={len(self.hand)}, citadel={len(self.citadel)})"