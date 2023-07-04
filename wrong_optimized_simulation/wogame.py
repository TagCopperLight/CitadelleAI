from random import shuffle

from wrong_optimized_simulation.player.woplayer import WOPlayer
from wrong_optimized_simulation.wobank import withdraw, deposit
import wrong_optimized_simulation.wobinary as ob

ROLES = ["Assassin", "Voleur", "Magicien", "Roi", "Eveque", "Marchand", "Architecte", "Condottiere"]


# Forced to a 5 player game
class WOGame:
    def __init__(self, players: list[WOPlayer], odisctricts: list[tuple[int, int]], debug: bool = False) -> None:
        self.players = players
        self.odistricts = odisctricts

        self.districts = list(range(54))
        self.bank = 30 - (5 * 2)
        self.crown = 0

        self.data: int = 70936231936 # Gave 2 golds per player

        self.hands = [0 for _ in range(5)]
        self.citadels = [0 for _ in range(5)]
        self.citadels_size = [0 for _ in range(5)]

        self.game_data = (self.data, self.hands, self.citadels)

        self.first_to_finish = -1

        self.DEBUG = debug

    def init(self) -> None:
        # TODO:
        shuffle(self.districts)

        for player in self.players:
            for i in range(4):
                self.hands[player.id] = ob.set_district(self.hands[player.id], self.districts[i], 1)
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
            role = self.players[id].select_character(self.data, self.hands, self.citadels, available_characters, unavailable_characters)
            self.data = ob.set_role(self.data, id, role)
            roles.remove(role)

    def play(self) -> None:
        roles = list(range(8))

        for player in self.players:
            self.debug(f"Player {player.id}: {ROLES[ob.get_role(self.data, player.id)]}")
        self.debug("")

        while len(roles) > 0:
            role = roles.pop(0)
            player = [player for player in range(5) if ob.get_role(self.data, player) == role]
            if not player: continue
            player = player[0]

            # ----------- Roles ------------

            match role:
                case 0:
                    # Assassin
                    focused_role = self.players[player].action(self.data, self.hands, self.citadels, self.odistricts)[1]
                    roles.remove(focused_role)
                    self.debug(f"Player {player} ({ROLES[role]}) killed {ROLES[focused_role]}")

                case 1:
                    # Thief
                    focused_role = self.players[player].action(self.data, self.hands, self.citadels, self.odistricts)[1]
                    focused_player = [player for player in range(5) if ob.get_role(self.data, player) == focused_role]
                    if focused_player:
                        focused_player = focused_player[0]

                        player_money = ob.get_money(self.data, player)
                        focused_player_money = ob.get_money(self.data, focused_player)

                        self.data = ob.set_money(self.data, player, player_money + focused_player_money)
                        self.data = ob.set_money(self.data, focused_player, 0)
                        self.debug(f"Player {player} ({ROLES[role]}) stole {focused_player_money} from player {focused_player} ({ROLES[focused_role]})")

                case 2:
                    # Magician
                    focused_role = self.players[player].action(self.data, self.hands, self.citadels, self.odistricts)[1]
                    focused_player = [player for player in range(5) if ob.get_role(self.data, player) == focused_role]
                    if focused_player:
                        focused_player = focused_player[0]

                        for district in range(54):
                            player_district = ob.get_district(self.hands[player], district)
                            focused_player_district = ob.get_district(self.hands[focused_player], district)

                            self.hands[player] = ob.set_district(self.hands[player], district, focused_player_district)
                            self.hands[focused_player] = ob.set_district(self.hands[focused_player], district, player_district)
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
                    self.data = ob.set_money(self.data, player, ob.get_money(self.data, player) + value_withdrawn)
                    self.calculate_incomes(player, 3)
                
                case 6:
                    # Architect
                    pass
                
                case 7:
                    # Condottiere
                    self.calculate_incomes(player, 4)

                    focused_role = self.players[player].action(self.data, self.hands, self.citadels, self.odistricts)[1]
                    focused_player = [player for player in range(5) if ob.get_role(self.data, player) == focused_role]
                    if focused_player:
                        focused_player = focused_player[0]

                        citadel: list[int] = []
                        for district in range(54):
                            if ob.get_district(self.citadels[focused_player], district):
                                citadel.append(district)
                        
                        if citadel:
                            district_to_destroy = min(citadel, key=lambda district: self.odistricts[district][0])
                            cost = self.odistricts[district_to_destroy][0]
                            if cost - 1 < ob.get_money(self.data, player) and self.citadels_size[focused_player] <= 7 and focused_role != 4:
                                self.data = ob.set_money(self.data, player, ob.get_money(self.data, player) - cost + 1)
                                self.bank= deposit(self.bank, cost - 1)

                                self.citadels[focused_player] = ob.set_district(self.citadels[focused_player], district_to_destroy, 0)
                                self.citadels_size[focused_player] -= 1

                                self.debug(f"Player {player} ({ROLES[role]}) destroyed district {district_to_destroy} from player {focused_player} ({ROLES[focused_role]})")
                
                case _:
                    raise Exception("Invalid role")
                
            # ----------- Actions ------------

            if role == 6:
                ammount_to_withdraw = 4
                ammount_to_pick = 2
            else:
                ammount_to_withdraw = 2
                ammount_to_pick = 1
            
            if self.players[player].choose_money_district(self.data, self.hands, self.citadels):
                self.bank, value_withdrawn = withdraw(self.bank, ammount_to_withdraw)
                self.data = ob.set_money(self.data, player, ob.get_money(self.data, player) + value_withdrawn)
                self.debug(f"Player {player} ({ROLES[role]}) withdrew {value_withdrawn} from the bank")
            else:
                for _ in range(ammount_to_pick):
                    if not self.districts: break
                    district = self.districts.pop(0)
                    self.hands[player] = ob.set_district(self.hands[player], district, 1)
                self.debug(f"Player {player} ({ROLES[role]}) picked {ammount_to_pick} districts from the deck")

            to_build = self.players[player].action(self.data, self.hands, self.citadels, self.odistricts)[0]

            if to_build != -1:
                player_money = ob.get_money(self.data, player)
                if player_money < self.odistricts[to_build][0]: continue
                self.data = ob.set_money(self.data, player, player_money - self.odistricts[to_build][0])
                self.bank = deposit(self.bank, self.odistricts[to_build][0])
                
                self.citadels[player] = ob.set_district(self.citadels[player], to_build, 1)
                self.hands[player] = ob.set_district(self.hands[player], to_build, 0)

                self.citadels_size[player] += 1
                self.debug(f"Player {player} ({ROLES[role]}) built district {to_build}")

                if self.citadels_size[player] >= 7:
                    self.first_to_finish = player
                    self.debug(f"Player {player} ({ROLES[role]}) finished his citadel")
    
    def calculate_incomes(self, player: int, color: int) -> None:
        for district in range(54):
            if ob.get_district(self.citadels[player], district) == 0: continue
            if self.odistricts[district][1] == color:
                self.bank, value_withdrawn = withdraw(self.bank, 1)
                self.data = ob.set_money(self.data, player, ob.get_money(self.data, player) + value_withdrawn)
    
    def calculate_scores(self) -> list[tuple[int, int]]:
        scores: list[tuple[int, int]] = []

        for player in range(5):
            score = 0
            for district in range(54):
                if ob.get_district(self.citadels[player], district) == 1:
                    score += self.odistricts[district][0]
            
            if self.first_to_finish == player:
                score += 4
            elif self.citadels_size[player] >= 7:
                score += 2

            colors = [False, False, False, False]
            for district in range(54):
                if ob.get_district(self.citadels[player], district) == 1:
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
        ob.print_data(self.data)
        ob.print_districts("Hands", self.hands)
        ob.print_districts("Citadels", self.citadels)
        return f"Game(Bank : {self.bank}, Citadels Sizes : {self.citadels_size})"
    
    def debug(self, *args: int|str) -> None:
        if self.DEBUG:
            print(*args)