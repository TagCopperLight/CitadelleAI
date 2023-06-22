from role import Role
from district import District


ROLES = [
    Role("Assassin", 1),
    Role("Thief", 2),
    Role("Magician", 3),
    Role("King", 4),
    Role("Bishop", 5),
    Role("Merchant", 6),
    Role("Architect", 7),
    Role("Warlord", 8)
]

DISTRICTS = [
    District(1, "Manor", 3, 1),
    District(2, "Castle", 4, 0),
    District(3, "Palace", 5, 1),
    District(4, "Watchtower", 1, 0),
    District(5, "Prison", 2, 4),
    District(6, "Battlefield", 3, 4),
    District(7, "Tavern", 1, 3),
    District(8, "Market", 2, 3),
    District(9, "Trading Post", 2, 3),
    District(10, "Docks", 3, 0),
    District(11, "Harbor", 4, 0),
    District(12, "Town Hall", 5, 0),
    District(13, "Temple", 1, 2),
    District(14, "Church", 2, 2),
    District(15, "Monastery", 3, 2),
    District(16, "Cathedral", 5, 2),
    District(17, "Observatory", 2, 0),
    District(18, "Smithy", 2, 0),
    District(19, "Laboratory", 5, 0),
    District(20, "Library", 6, 0),
    District(21, "School of Magic", 6, 0),
    District(22, "Great Wall", 3, 0),
    District(23, "Fortress", 5, 0)
]