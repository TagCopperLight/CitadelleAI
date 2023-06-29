from game_state import GameState
from player import Player
from role import Role
from district import District

from random import shuffle


class Game:
    def __init__(self, players: list[Player], roles: list[Role], districts: list[District]) -> None:
        self.game_state = GameState(districts, roles)
        self.players = players

        self.roles = roles

    def init(self) -> None:
        shuffle(self.game_state.districts)

        for player in self.players:
            player.money += 2
            self.game_state.bank -= 2

            player.hand = self.game_state.districts[:4]
            self.districts = self.game_state.districts[4:]

    def players_sort(self) -> None:
        players = [player for player in self.players if player.id == self.game_state.current_player_id]

        for id in list(range(self.game_state.current_player_id + 1, len(self.players))) + list(range(0, self.game_state.current_player_id)):
            players += [player for player in self.players if player.id == id]

        self.players = players

    def select_characters(self) -> None:
        roles = self.game_state.roles.copy()
        shuffle(roles)
        unavailable_characters = [roles.pop(), roles.pop()]

        self.players_sort()

        for player in self.players:
            available_characters = roles
            player.role = player.select_character(self.game_state, available_characters, unavailable_characters)
            roles.remove(player.role)

    def play(self) -> None:
        players = sorted(self.players, key=lambda player: player.role.order)

        self.calculate_incomes()

        for player in players:
            print(player)
            if player.choose_money_district(self.game_state):
                player.money += 2
                self.game_state.bank -= 2
            else:
                player.hand.append(self.districts.pop())

            player.build_district(self.game_state)
            player.action(self.game_state)

    def calculate_incomes(self) -> None:
        # TODO: District and role effects
        for player in self.players:
            player.money += 0
            self.game_state.bank -= 0

    def __repr__(self) -> str:
        return f"Game(game_state={self.game_state}, players={self.players})"