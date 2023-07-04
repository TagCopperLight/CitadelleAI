from random import choice
import optimized_simulation.obinary as ob


class OPlayer:
    def __init__(self, id: int) -> None:
        self.id = id

    def select_character(self, data: int, hands: list[int], citadels: list[int], available_characters: list[int], unavailable_characters: list[int]) -> int:
        return choice(available_characters)
    
    def choose_money_district(self, data: int, hands: list[int], citadels: list[int]) -> bool:
        return choice([True, False])
    
    def action(self, data: int, hands: list[int], citadels: list[int], odistricts: list[tuple[int, int]]) -> tuple[int, int]:
        buildable_districts: list[int] = []
        for i in range(54):
            if ob.get_district(hands[self.id], i) and odistricts[i][0] <= ob.get_money(data, self.id):
                buildable_districts.append(i)

        if buildable_districts:
            to_build = choice(buildable_districts)
        else:
            to_build = -1

        return to_build, choice([role for role in range(8) if ob.get_role(data, self.id) != role])