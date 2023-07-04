from random import choice


class OPlayer:
    def __init__(self, id: int) -> None:
        self.id = id

    def select_character(self, moneys: list[int], hands: list[list[int]], citadels: list[list[int]], available_characters: list[int], unavailable_characters: list[int]) -> int:
        return choice(available_characters)
    
    def choose_money_district(self, moneys: list[int], hands: list[list[int]], citadels: list[list[int]], role: int) -> bool:
        return choice([True, False])
    
    def action(self, moneys: list[int], hands: list[list[int]], citadels: list[list[int]], role: int, odistricts: list[tuple[int, int]]) -> tuple[int, int]:
        buildable_districts: list[int] = []
        for district in hands[self.id]:
            if odistricts[district][0] <= moneys[self.id]:
                buildable_districts.append(district)
        
        buildable_districts.append(-1) # To make the game longer

        if buildable_districts:
            to_build = choice(buildable_districts)
        else:
            to_build = -1

        return to_build, choice([rol for rol in range(8) if rol != role])
    
    def __repr__(self) -> str:
        return f"OPlayer({self.id})"