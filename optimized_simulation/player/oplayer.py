class OPlayer:
    def __init__(self, id: int) -> None:
        self.id = id

    def select_character(self, data: int, hands: list[int], citadels: list[int], available_characters: list[int], unavailable_characters: list[int]) -> int:
        raise NotImplementedError
    
    def choose_money_district(self, data: int, hands: list[int], citadels: list[int]) -> bool:
        raise NotImplementedError
    
    def action(self, data: int, hands: list[int], citadels: list[int]) -> tuple[int, int]:
        raise NotImplementedError