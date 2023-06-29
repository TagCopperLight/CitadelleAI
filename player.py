from game_state import GameState
from district import District
from role import Role

from random import choice


class Player:
    def __init__(self, id: int) -> None:
        self.id = id

        self.money = 0
        self.role: Role = Role(0, "None")

        self.hand: list[District] = []
        self.citadel: list[District] = []
    
    def select_character(self, game_state: GameState, available_characters: list[Role], unavailable_characters: list[Role]) -> Role:
        return choice(available_characters)
    
    def choose_money_district(self, game_state: GameState) -> bool:
        return choice([True, False])

    def action(self, game_state: GameState) -> tuple[District, Role]:
        buildable_districts = [district for district in self.hand if district.cost <= self.money] + [District(0, "None", 0, 0)]*5
        if buildable_districts:
            to_build = choice(buildable_districts)
        else:
            to_build = District(0, "None", 0, 0)

        return to_build, choice([role for role in game_state.roles if role.order != self.role.order])
    
    def __repr__(self) -> str:
        return f"Player(id={self.id}, money={self.money}, role={self.role}, hand={len(self.hand)}, citadel={self.citadel})"