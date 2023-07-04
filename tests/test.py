def check_player(player: int) -> None:
    if player < 0 or player > 4:
        raise ValueError("Player must be between 0 and 4")
    
def check_value(value: int, value_min: int, value_max: int) -> None:
    if value < value_min or value > value_max:
        raise ValueError(f"Value must be between {value_min} and {value_max}")

def binary(num: int) -> str:
    return bin(num)[2:].zfill(64)

def get_money(data: int, player: int) -> int:
    # 5 bits per player + 15 bits for the roles
    check_player(player)
    return (data >> (player * 5 + 15)) & 0b11111

def set_money(data: int, player: int, value: int) -> int:
    # 5 bits per player + 15 bits for the roles
    check_player(player)
    check_value(value, 0, 31)
    return (data & ~(0b11111 << (player * 5 + 15))) | (value << (player * 5 + 15))

def get_role(data: int, player: int) -> int:
    # 3 bits per player
    check_player(player)
    return (data >> (player * 3)) & 0b111

def set_role(data: int, player: int, value: int) -> int:
    # 3 bits per player
    check_player(player)
    check_value(value, 0, 7)
    return (data & ~(0b111 << (player * 3))) | (value << (player * 3))

def get_district_in_hand(data: int, district: int) -> int:
    # 1 bit per district
    check_value(district, 0, 53)
    return (data >> district) & 0b1

def set_district_in_hand(data: int, district: int) -> int:
    # 1 bit per district
    check_value(district, 0, 53)
    return (data & ~(0b1 << district)) | (1 << district)

def get_select_order(crown: int) -> list[int]:
    order: list[int] = []
    order += list(range(crown, 8))
    order += list(range(0, crown))
    return order

for i in range(8):
    print(get_select_order(i))