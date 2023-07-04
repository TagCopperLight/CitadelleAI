from random import shuffle

from optimized_simulation.player.oplayer import OPlayer
from optimized_simulation.obank import withdraw, deposit


ROLES = ["Assassin", "Voleur", "Magicien", "Roi", "Eveque", "Marchand", "Architecte", "Condottiere"]

def cindex(list : list[int], index: int) -> int|None:
    try:
        return list.index(index)
    except ValueError:
        return None

# Forced to a 5 player game
class OGame:
    def __init__(self, players: list[OPlayer], odisctricts: list[tuple[int, int]], debug: bool = False) -> None:
        self.players = players
        self.odistricts = odisctricts

        self.districts = list(range(54))
        self.bank = 30 - (5 * 2)
        self.crown = 0

        self.moneys = [2 for _ in range(5)]
        self.roles = [-1 for _ in range(5)]

        self.hands: list[list[int]] = [[] for _ in range(5)]
        self.citadels: list[list[int]] = [[] for _ in range(5)]
        self.citadels_size = [0 for _ in range(5)]

        self.first_to_finish = -1

        self.DEBUG = debug

    def init(self) -> None:
        shuffle(self.districts)

        for player in self.players:
            for _ in range(4):
                self.hands[player.id].append(self.districts.pop(0))
            self.districts = self.districts[4:]
    
    def get_select_order(self) -> list[int]:
        order: list[int] = []
        order += list(range(self.crown, 5))
        order += list(range(0, self.crown))
        return order
    
    def select_characters(self) -> None:
        # TODO: Enlever un role de plus et le rajouter à la fin
        roles = list(range(8))
        shuffle(roles)
        unavailable_characters = [roles.pop(), roles.pop()]

        order = self.get_select_order()

        for id in order:
            available_characters = roles
            role = self.players[id].select_character(self.moneys, self.hands, self.citadels, available_characters, unavailable_characters)
            self.roles[id] = role
            roles.remove(role)

    def play(self) -> None:
        roles = list(range(8))

        for player in self.players:
            self.debug(f"Player {player.id}: {ROLES[self.roles[player.id]]}")
        self.debug("")

        while len(roles) > 0:
            role = roles.pop(0)
            player = cindex(self.roles, role)
            if player == None: continue

            # ----------- Roles ------------

            match role:
                case 0:
                    # Assassin
                    focused_role = self.players[player].action(self.moneys, self.hands, self.citadels, role, self.odistricts)[1]
                    roles.remove(focused_role)
                    self.debug(f"Player {player} ({ROLES[role]}) killed {ROLES[focused_role]}")

                case 1:
                    # Thief
                    focused_role = self.players[player].action(self.moneys, self.hands, self.citadels, role, self.odistricts)[1]
                    focused_player = cindex(self.roles, focused_role)
                    if focused_player != None:
                        player_money = self.moneys[player]
                        focused_player_money = self.moneys[focused_player]

                        self.moneys[player] = player_money + focused_player_money
                        self.moneys[focused_player] = 0
                        self.debug(f"Player {player} ({ROLES[role]}) stole {focused_player_money} from player {focused_player} ({ROLES[focused_role]})")

                case 2:
                    # Magician
                    focused_role = self.players[player].action(self.moneys, self.hands, self.citadels, role, self.odistricts)[1]
                    focused_player = cindex(self.roles, focused_role)
                    if focused_player != None:
                        player_hand = self.hands[player].copy()
                        focused_player_hand = self.hands[focused_player].copy()

                        self.hands[player] = focused_player_hand
                        self.hands[focused_player] = player_hand
                        self.debug(f"Player {player} ({ROLES[role]}) swapped hands with player {focused_player} ({ROLES[focused_role]})")
                
                case 3:
                    # King
                    self.crown = player
                    self.calculate_incomes(player, 1)
                    self.debug(f"Player {player} ({ROLES[role]}) took the crown")
                
                case 4:
                    # Bishop
                    self.calculate_incomes(player, 2)

                case 5:
                    # Merchant
                    self.bank, value_withdrawn = withdraw(self.bank, 1)
                    self.moneys[player] += value_withdrawn
                    self.calculate_incomes(player, 3)
                
                case 6:
                    # Architect
                    pass
                
                case 7:
                    # Condottiere
                    self.calculate_incomes(player, 4)

                    focused_role = self.players[player].action(self.moneys, self.hands, self.citadels, role, self.odistricts)[1]
                    focused_player = cindex(self.roles, focused_role)
                    if focused_player != None and self.citadels_size[focused_player] > 0:
                        district_to_destroy = min(self.citadels[focused_player], key=lambda district: self.odistricts[district][0])
                        cost = self.odistricts[district_to_destroy][0]
                        if cost - 1 < self.moneys[player] and self.citadels_size[focused_player] <= 7 and focused_role != 4:
                            self.moneys[player] -= (cost - 1)
                            self.bank= deposit(self.bank, cost - 1)

                            self.citadels[focused_player].remove(district_to_destroy)
                            self.citadels_size[focused_player] -= 1

                            self.districts.append(district_to_destroy)

                            self.debug(f"Player {player} ({ROLES[role]}) destroyed district {district_to_destroy} from player {focused_player} ({ROLES[focused_role]})")
                
                case _:
                    raise Exception("Invalid role")
                
            # ----------- Actions ------------

            if role == 6:
                ammount_to_withdraw, ammount_to_pick = 4, 2
            else:
                ammount_to_withdraw, ammount_to_pick = 2, 1
            
            if self.players[player].choose_money_district(self.moneys, self.hands, self.citadels, role):
                self.bank, value_withdrawn = withdraw(self.bank, ammount_to_withdraw)
                self.moneys[player] += value_withdrawn
                self.debug(f"Player {player} ({ROLES[role]}) withdrew {value_withdrawn} from the bank")
            else:
                for _ in range(ammount_to_pick):
                    if not self.districts: break
                    district = self.districts.pop(0)
                    self.hands[player].append(district)
                self.debug(f"Player {player} ({ROLES[role]}) picked {ammount_to_pick} districts from the deck")

            to_build = self.players[player].action(self.moneys, self.hands, self.citadels, role, self.odistricts)[0]

            if to_build != -1:
                player_money = self.moneys[player]
                if player_money < self.odistricts[to_build][0]: continue
                self.moneys[player] -= self.odistricts[to_build][0]
                self.bank = deposit(self.bank, self.odistricts[to_build][0])
                
                self.citadels[player].append(to_build)
                self.hands[player].remove(to_build)

                self.citadels_size[player] += 1
                self.debug(f"Player {player} ({ROLES[role]}) built district {to_build}")

                if self.citadels_size[player] >= 7:
                    self.first_to_finish = player
                    self.debug(f"Player {player} ({ROLES[role]}) finished his citadel")
    
    def calculate_incomes(self, player: int, color: int) -> None:
        for district in self.citadels[player]:
            if self.odistricts[district][1] == color:
                self.bank, value_withdrawn = withdraw(self.bank, 1)
                self.moneys[player] += value_withdrawn
    
    def calculate_scores(self) -> list[tuple[int, int]]:
        scores: list[tuple[int, int]] = []

        for player in range(5):
            score = 0
            for district in self.citadels[player]:
                score += self.odistricts[district][0]
            
            if self.first_to_finish == player:
                score += 4
            elif self.citadels_size[player] >= 7:
                score += 2

            colors = [False, False, False, False]
            for district in self.citadels[player]:
                colors[self.odistricts[district][1] - 1] = True
            
            if all(colors):
                score += 3
            
            scores.append((player, score))

        return scores
    
    def game_over(self) -> tuple[bool, int]:
        scores = self.calculate_scores()
        ended = any([self.citadels_size[player] >= 7 for player in range(5)])
        max_score = (-1, 0)
        if ended:
            max_score = max(scores, key=lambda score: score[1])
            if len([score for score in scores if score[1] == max_score[1]]) > 1:
                max_score = (-1, 0)

        return ended, max_score[0]
    
    def __repr__(self) -> str:
        print(f"Moneys : {self.moneys}")
        print(f"Hands : {self.hands}")
        print(f"Citadels : {self.citadels}")
        return f"Game(Bank : {self.bank}, Citadels Sizes : {self.citadels_size})"
    
    def debug(self, *args: int|str) -> None:
        if self.DEBUG:
            print(*args)