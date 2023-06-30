from game_state import GameState
from player import Player
from role import Role
from district import District

from random import shuffle


class Game:
    def __init__(self, players: list[Player], roles: list[Role], districts: list[District]) -> None:
        self.game_state = GameState(districts, roles)
        self.players = players

        self.first_to_finish = -1

        self.roles = roles

    def init(self) -> None:
        shuffle(self.game_state.districts)

        for player in self.players:
            player.money += self.game_state.bank.withdraw(2)

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
                player.money += self.game_state.bank.withdraw(2)
            else:
                # print(f"Player {player.id} ({player.role}) takes 1 card", "\n")
                if self.game_state.districts:
                    player.hand.append(self.game_state.districts.pop())

            to_build, _ = player.action(self.game_state)

            # TODO: Validate the build 
            if to_build.id != 0:
                # print(f"Player {player.id} ({player.role}) builds {to_build}", "\n")
                player.money -= self.game_state.bank.deposit(to_build.cost)

                player.hand.remove(to_build)
                player.citadel.append(to_build)
                if len(player.citadel) >= 7:
                    self.first_to_finish = player.id

            # TODO: Role effects
        
    def calculate_incomes(self) -> None:
        # TODO: District and role effects
        for player in self.players:
            player.money += self.game_state.bank.withdraw(0)

    def calculate_scores(self) -> list[tuple[Player, int]]:
        scores: list[tuple[Player, int]] = []

        for player in self.players:
            score = 0
            for district in player.citadel:
                score += district.cost

            if player.id == self.first_to_finish:
                score += 4
            elif len(player.citadel) >= 7:
                score += 2
            
            colors = [False, False, False, False]
            for district in player.citadel:
                colors[district.color - 1] = True
            
            if all(colors):
                score += 3

            scores.append((player, score))
        return scores

    def game_over(self) -> tuple[bool, Player]:
        ended = any([len(player.citadel) >= 7 for player in self.players])
        scores = [score for _, score in self.calculate_scores()]
        if any(scores.count(x) > 1 for x in scores):
            return ended, Player(-1)
        return ended, max(self.calculate_scores(), key=lambda score: score[1])[0]
    
    def __repr__(self) -> str:
        return f"Game(game_state={self.game_state}, players={self.players})"