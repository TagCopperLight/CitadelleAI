from game import Game
from data import ROLES, DISTRICTS
from player import Player

players = [Player(0), Player(1), Player(2), Player(3)]

game = Game(players, ROLES, DISTRICTS)
print(game)
game.init()
print(game)
game.select_characters()
print(game)
game.play()
print(game)