from optimized_simulation.player.oplayer import OPlayer

from random import choice


class OBasicPlayer(OPlayer):
    def select_character(self, moneys: list[int], hands: list[list[int]], citadels: list[list[int]], available_characters: list[int], unavailable_characters: list[int]) -> int:
        prefered_roles = [5, 1, 6, 3, 4, 0, 7, 2]
        
        for role in prefered_roles:
            if role in available_characters:
                return role
        raise Exception("No role available")

    def choose_money_district(self, moneys: list[int], hands: list[list[int]], citadels: list[list[int]], role: int) -> bool:
        if len(hands[self.id]) == 3:
            return False
        else:
            return True
    
    def action(self, moneys: list[int], hands: list[list[int]], citadels: list[list[int]], role: int, odistricts: list[tuple[int, int]]) -> tuple[int, int]:
        buildable_districts: list[int] = []
        for district in hands[self.id]:
            if odistricts[district][0] <= moneys[self.id]:
                buildable_districts.append(district)
        
        if buildable_districts:
            to_build = choice(buildable_districts)
        else:
            to_build = -1

        role_to_target = 7
        if role == role_to_target:
            role_to_target += 1
            role_to_target %= 8

        return to_build, role_to_target