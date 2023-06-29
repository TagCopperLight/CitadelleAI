from game import Game
from data import ROLES, DISTRICTS
from player import Player

from matplotlib import pyplot as plt
from progress.bar import IncrementalBar #type: ignore


def play_game() -> int:
    players = [Player(0), Player(1), Player(2), Player(3), Player(4)]

    game = Game(players, ROLES, DISTRICTS)
    game.init()

    turn = 0

    while True:
        print(game, "\n")
        game.select_characters()
        print(game, "\n")
        game.play()
        print(game, "\n")

        if game.game_over()[0]:
            print([score for _, score in game.calculate_scores()], "\n")
            return game.game_over()[1].id

        turn += 1

x: list[int] = []
bins = [x + 0.5 for x in range(-1, 5)]

ties = 0

iterations = 1
with IncrementalBar('Playing games', max = iterations) as bar:
    for i in range(iterations):
        winner = play_game()
        x.append(winner)
        if winner == -1:
            ties += 1
        bar.next()

plt.hist(x, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore
print(f"Ties: {ties}")
plt.show() #type: ignore