from game_state import GameState
from player.player import Player
from role import Role
from district import District

from random import shuffle


class Game:
    def __init__(self, players: list[Player], roles: list[Role], districts: list[District], debug: bool = False) -> None:
        self.game_state = GameState(districts, roles)
        self.players = players

        self.first_to_finish = -1

        self.roles = roles

        self.DEBUG = debug

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

    def select_characters(self) -> None:
        #TODO: Enlever un role de plus et le rajouter à la fin
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

        for player in players:
            self.debug(f"Player {player.id}: {player.role}")
        self.debug("")

        while len(players) > 0:
            player = players.pop(0)

            # ----------- Roles ------------
            if player.role.order == 0:
                focused_role = player.action(self.game_state)[1]
                focused_player = [player for player in self.players if player.role == focused_role]
                self.debug(f"Player {player.id} ({player.role}) tried to kill {focused_role}")
                if focused_player:
                    self.debug(f"Player {player.id} ({player.role}) kills Player {focused_player[0].id} ({focused_player[0].role})")
                    players.remove(focused_player[0])

            elif player.role.order == 1:
                focused_role = player.action(self.game_state)[1]
                focused_player = [player for player in self.players if player.role == focused_role]
                self.debug(f"Player {player.id} ({player.role}) tried to steal from {focused_role}")
                if focused_player:
                    self.debug(f"Player {player.id} ({player.role}) steals {focused_player[0].money} gold from Player {focused_player[0].id} ({focused_player[0].role})")
                    player.money += focused_player[0].money
                    focused_player[0].money = 0

            elif player.role.order == 2:
                # TODO: Focus a player not a role
                focused_role = player.action(self.game_state)[1]
                focused_player = [player for player in self.players if player.role == focused_role]
                self.debug(f"Player {player.id} ({player.role}) tried to swap hands with {focused_role}")
                if focused_player:
                    self.debug(f"Player {player.id} ({player.role}) swaps hands with Player {focused_player[0].id} ({focused_player[0].role})")
                    hand = focused_player[0].hand.copy()
                    focused_player[0].hand = player.hand.copy()
                    player.hand = hand

            elif player.role.order == 3:
                self.debug(f"Player {player.id} ({player.role}) gets the crown")
                self.game_state.current_player_id = player.id
                self.calculate_incomes(player, 1)
            
            elif player.role.order == 4:
                self.calculate_incomes(player, 2)
            
            elif player.role.order == 5:
                player.money += self.game_state.bank.withdraw(1)
                self.calculate_incomes(player, 3)

            elif player.role.order == 7:
                self.calculate_incomes(player, 4)
                # TODO: Focus a player not a role
                focused_role = player.action(self.game_state)[1]
                focused_player = [player for player in self.players if player.role == focused_role]
                if focused_player and focused_player[0].citadel:
                    district_to_destroy = min(focused_player[0].citadel, key=lambda district: district.cost)
                    cost = district_to_destroy.cost
                    if player.money < cost - 1:
                        if len(focused_player[0].citadel) < 7 or focused_player[0].role.order != 4:
                            player.money -= self.game_state.bank.deposit(cost - 1)
                            self.debug(f"Player {player.id} ({player.role}) destroys {district_to_destroy} from Player {focused_player[0].id} ({focused_player[0].role})")
                            focused_player[0].citadel.remove(district_to_destroy)

            # ----------- Actions ------------
            if player.role.order == 6:
                if player.choose_money_district(self.game_state):
                    self.debug(f"Player {player.id} ({player.role}) takes 4 gold", "\n")
                    player.money += self.game_state.bank.withdraw(4)
                else:
                    self.debug(f"Player {player.id} ({player.role}) takes 2 card", "\n")
                    for _ in range(2):
                        if self.game_state.districts:
                            player.hand.append(self.game_state.districts.pop())
            else:
                if player.choose_money_district(self.game_state):
                    self.debug(f"Player {player.id} ({player.role}) takes 2 gold", "\n")
                    player.money += self.game_state.bank.withdraw(2)
                else:
                    self.debug(f"Player {player.id} ({player.role}) takes 1 card", "\n")
                    if self.game_state.districts:
                        player.hand.append(self.game_state.districts.pop())

            to_build, _ = player.action(self.game_state)

            # TODO: Validate the build 
            if to_build.id != 0:
                self.debug(f"Player {player.id} ({player.role}) built {to_build}", "\n")
                player.money -= self.game_state.bank.deposit(to_build.cost)

                player.hand.remove(to_build)
                player.citadel.append(to_build)
                if len(player.citadel) >= 7:
                    self.first_to_finish = player.id

    def calculate_incomes(self, player: Player, color: int) -> None:
        for district in player.citadel:
            if district.color == color:
                player.money += self.game_state.bank.withdraw(1)

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
        max_score = (Player(-1), 0)
        if ended:
            max_score = max(self.calculate_scores(), key=lambda score: score[1])
            if len([score for score in self.calculate_scores() if score[1] == max_score[1]]) > 1:
                max_score = (Player(-1), 0)

        return ended, max_score[0]
    
    def __repr__(self) -> str:
        return f"Game(game_state={self.game_state}, players={self.players})"
    
    def debug(self, *args: int|str|Role) -> None:
        if self.DEBUG:
            print(*args)