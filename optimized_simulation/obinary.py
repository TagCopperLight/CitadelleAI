def binary(num: int) -> str:
    return bin(num)[2:].zfill(64)

def get_money(data: int, player: int) -> int:
    # 5 bits per player + 15 bits for the roles
    return (data >> (player * 5 + 15)) & 0b11111

def set_money(data: int, player: int, value: int) -> int:
    # 5 bits per player + 15 bits for the roles
    return (data & ~(0b11111 << (player * 5 + 15))) | (value << (player * 5 + 15))

def get_role(data: int, player: int) -> int:
    # 3 bits per player
    return (data >> (player * 3)) & 0b111

def set_role(data: int, player: int, value: int) -> int:
    # 3 bits per player
    return (data & ~(0b111 << (player * 3))) | (value << (player * 3))

def get_district(data: int, district: int) -> int:
    # 1 bit per district
    return (data >> district) & 0b1

def set_district(data: int, district: int, value: int) -> int:
    # 1 bit per district
    return (data & ~(0b1 << district)) | (value << district)

def print_data(data: int) -> None:
    money = "["
    for i in range(4):
        money += f"{get_money(data, i)}, "
    money += f"{get_money(data, 4)}]"
    print(f"Money: {money}")

def print_districts(header: str, data: list[int]) -> None:
    districts: list[str] = []
    for district in data:
        dis = "["
        for i in range(53):
            if get_district(district, i) == 1:
                dis += f"{i}, "
        if get_district(district, 53) == 1:
            dis += "53"
        dis += "]"
        districts.append(dis)
    print(f"{header}: {districts}")