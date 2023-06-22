from game import Game
from data import ROLES, DISTRICTS

game = Game(4, ROLES, DISTRICTS)
print(game)
game.init()
print(game)
game.select_characters()
print(game)
game.play()
print(game)