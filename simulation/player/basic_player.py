from simulation.player.player import Player

from simulation.game_state import GameState
from simulation.role import Role
from simulation.district import District

from random import choice


class BasicPlayer(Player):
    def select_character(self, game_state: GameState, available_characters: list[Role], unavailable_characters: list[Role]) -> Role:
        # for role in available_characters:
        #     if role.order == 5:
        #         return role
        return choice(available_characters)
    
    def choose_money_district(self, game_state: GameState) -> bool:
        return choice([True, False])

    def action(self, game_state: GameState) -> tuple[District, Role]:
        buildable_districts = [district for district in self.hand if district.cost <= self.money]
        if buildable_districts:
            to_build = choice(buildable_districts)
        else:
            to_build = District(0, "None", 0, 0)

        return to_build, choice([role for role in game_state.roles if role.order != self.role.order])