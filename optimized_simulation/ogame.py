from random import shuffle

from optimized_simulation.player.oplayer import OPlayer
from optimized_simulation.obank import withdraw, deposit
import optimized_simulation.obinary as ob


# Forced to a 5 player game
class OGame:
    def __init__(self, players: list[OPlayer], odisctricts: list[tuple[int, int]], debug: bool = False) -> None:
        self.players = players
        self.odistricts = odisctricts

        self.districts = list(range(54))
        self.bank = 30 - (5 * 2)
        self.crown = 0

        self.data = 70936231936 # Gave 2 golds per player

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
                ob.set_district(self.hands[player.id], self.districts[i], 1)
            self.districts = self.districts[4:]
    
    def get_select_order(self) -> list[int]:
        order: list[int] = []
        order += list(range(self.crown, 8))
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
            role = self.players[id].select_character(*self.game_data, available_characters, unavailable_characters)
            ob.set_role(self.data, id, role)
            roles.remove(role)

    def play(self) -> None:
        roles = list(range(8))

        while len(roles) > 0:
            role = roles.pop(0)
            player = [player for player in range(5) if ob.get_role(self.data, player) == role]
            if not player: continue
            player = player[0]

            # ----------- Roles ------------

            match role:
                case 0:
                    # Assassin
                    focused_role = self.players[player].action(*self.game_data, self.odistricts)[1]
                    roles.remove(focused_role)

                case 1:
                    # Thief
                    focused_role = self.players[player].action(*self.game_data, self.odistricts)[1]
                    focused_player = [player for player in range(5) if ob.get_role(self.data, player) == focused_role]
                    if not focused_player: continue
                    focused_player = focused_player[0]

                    player_money = ob.get_money(self.data, player)
                    focused_player_money = ob.get_money(self.data, focused_player)

                    ob.set_money(self.data, player, player_money + focused_player_money)
                    ob.set_money(self.data, focused_player, 0)

                case 2:
                    # Magician
                    focused_role = self.players[player].action(*self.game_data, self.odistricts)[1]
                    focused_player = [player for player in range(5) if ob.get_role(self.data, player) == focused_role]
                    if not focused_player: continue
                    focused_player = focused_player[0]

                    for district in range(54):
                        player_district = ob.get_district(self.hands[player], district)
                        focused_player_district = ob.get_district(self.hands[focused_player], district)

                        ob.set_district(self.hands[player], district, focused_player_district)
                        ob.set_district(self.hands[focused_player], district, player_district)
                
                case 3:
                    # King
                    self.crown = player
                    self.calculate_incomes(player, 1)
                
                case 4:
                    # Bishop
                    self.calculate_incomes(player, 2)

                case 5:
                    # Merchant
                    self.bank, value_withdrawn = withdraw(self.bank, 1)
                    ob.set_money(self.data, player, ob.get_money(self.data, player) + value_withdrawn)
                    self.calculate_incomes(player, 3)
                
                case 6:
                    # Architect
                    pass
                
                case 7:
                    # Condottiere
                    self.calculate_incomes(player, 4)

                    focused_role = self.players[player].action(*self.game_data, self.odistricts)[1]
                    focused_player = [player for player in range(5) if ob.get_role(self.data, player) == focused_role]
                    if not focused_player: continue
                    focused_player = focused_player[0]

                    citadel: list[int] = []
                    for district in range(54):
                        if ob.get_district(self.citadels[focused_player], district):
                            citadel.append(district)
                    
                    if not citadel: continue
                    district_to_destroy = min(citadel, key=lambda district: self.odistricts[district][0])
                    cost = self.odistricts[district_to_destroy][0]
                    if cost - 1 > ob.get_money(self.data, player): continue
                    if self.citadels_size[focused_player] >= 7: continue
                    if focused_role == 4: continue

                    ob.set_money(self.data, player, ob.get_money(self.data, player) - cost + 1)
                    deposit(self.bank, cost - 1)

                    ob.set_district(self.citadels[focused_player], district_to_destroy, 0)
                    self.citadels_size[focused_player] -= 1
                
                case _:
                    raise Exception("Invalid role")
                
            # ----------- Actions ------------

            if role == 6:
                ammount_to_withdraw = 4
                ammount_to_pick = 2
            else:
                ammount_to_withdraw = 2
                ammount_to_pick = 1
            
            if self.players[player].choose_money_district(*self.game_data):
                self.bank, value_withdrawn = withdraw(self.bank, ammount_to_withdraw)
                ob.set_money(self.data, player, ob.get_money(self.data, player) + value_withdrawn)
            else:
                for _ in range(ammount_to_pick):
                    if not self.districts: break
                    district = self.districts.pop(0)
                    ob.set_district(self.hands[player], district, 1)

            to_build = self.players[player].action(*self.game_data, self.odistricts)[0]

            if to_build != -1:
                player_money = ob.get_money(self.data, player)
                if player_money < self.odistricts[to_build][0]: continue
                ob.set_money(self.data, player, player_money - self.odistricts[to_build][0])
                deposit(self.bank, self.odistricts[to_build][0])
                
                ob.set_district(self.citadels[player], to_build, 1)
                ob.set_district(self.hands[player], to_build, 0)

                self.citadels_size[player] += 1

                if self.citadels_size[player] >= 7:
                    self.first_to_finish = player
    
    def calculate_incomes(self, player: int, color: int) -> None:
        for district in range(54):
            if ob.get_district(self.citadels[player], district) == 0: continue
            if self.odistricts[district][1] == color:
                self.bank, value_withdrawn = withdraw(self.bank, 1)
                ob.set_money(self.data, player, ob.get_money(self.data, player) + value_withdrawn)
    
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
                    colors[self.odistricts[district][1]] = True
            
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