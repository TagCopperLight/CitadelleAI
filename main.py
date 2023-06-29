from game import Game
from data import ROLES, DISTRICTS
from player import Player

players = [Player(0), Player(1), Player(2), Player(3), Player(4)]

game = Game(players, ROLES, DISTRICTS)
print(game, "\n")
game.init()
print(game, "\n")
game.select_characters()
print(game, "\n")
game.play()
print(game, "\n")