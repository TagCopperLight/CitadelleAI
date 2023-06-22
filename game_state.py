from player import Player
from district import District


class GameState:
    def __init__(self, players: int) -> None:
        self.bank = 30
        self.districts: list[District]

        self.players = [Player() for _ in range(players)]

    def init(self):
        for player in self.players:
            player.money += 2
            self.bank -= 2