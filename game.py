from game_state import GameState
from player import Player

from random import shuffle


class Game:
    def __init__(self, players: int) -> None:
        self.game_state = GameState()
        self.players = [Player(id) for id in range(players)]

    def init(self) -> None:
        shuffle(self.game_state.districts)

        for player in self.players:
            player.money += 2
            self.game_state.bank -= 2

            player.hand = self.game_state.districts[:4]
            self.districts = self.game_state.districts[4:]

    def select_characters(self) -> None:
        roles = self.game_state.roles.copy()
        shuffle(roles)

        unavailable_characters = [roles.pop(), roles.pop()]
        for player in self.players:
            available_characters = roles
            player.role = player.select_character(self.game_state, available_characters, unavailable_characters)
            roles.remove(player.role)