from game_state import GameState
from district import District
from role import Role


class Player:
    def __init__(self, id: int) -> None:
        self.id = id

        self.money: int
        self.role: Role

        self.hand: list[District]
        self.citadel: list[District]
    
    def select_character(self, game_state: GameState, available_characters: list[Role], unavailable_characters: list[Role]) -> Role:
        return available_characters[0]