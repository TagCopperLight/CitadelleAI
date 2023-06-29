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
            self.game_state.districts = self.game_state.districts[4:]

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
            # print(f"Player {player.id} selects {player.role}", "\n")
            roles.remove(player.role)

    def play(self) -> None:
        players = sorted(self.players, key=lambda player: player.role.order)

        self.calculate_incomes()

        for player in players:
            if player.choose_money_district(self.game_state):
                # print(f"Player {player.id} ({player.role}) takes 2 gold", "\n")
                player.money += 2
                self.game_state.bank -= 2
            else:
                # print(f"Player {player.id} ({player.role}) takes 1 card", "\n")
                if self.game_state.districts:
                    player.hand.append(self.game_state.districts.pop())

            to_build, _ = player.action(self.game_state)

            # TODO: Validate the build 
            if to_build.id != 0:
                # print(f"Player {player.id} ({player.role}) builds {to_build}", "\n")
                self.game_state.bank += to_build.cost
                player.money -= to_build.cost

                player.hand.remove(to_build)
                player.citadel.append(to_build)

            # TODO: Role effects

    def calculate_incomes(self) -> None:
        # TODO: District and role effects
        for player in self.players:
            player.money += 0
            self.game_state.bank -= 0

    def game_over(self) -> tuple[bool, Player, int]:
        ended = any([len(player.citadel) >= 7 for player in self.players])
        return ended, [player for player in self.players if len(player.citadel) >= 7][-1] if ended else Player(-1)
    
    def __repr__(self) -> str:
        return f"Game(game_state={self.game_state}, players={self.players})"