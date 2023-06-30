from game import Game
from data import ROLES, DISTRICTS
from player import Player

from matplotlib import pyplot as plt
from progress.bar import IncrementalBar #type: ignore


def play_game() -> tuple[int, list[tuple[Player, int]]]:
    players = [Player(0), Player(1), Player(2), Player(3), Player(4)]

    game = Game(players, ROLES, DISTRICTS)
    game.init()

    turn = 0

    while True:
        game.select_characters()
        game.play()

        if game.game_over()[0]:
            return game.game_over()[1].id, game.calculate_scores()

        turn += 1

winner_list: list[int] = []
score_list: list[int] = []

ties = 0

iterations = 10000
with IncrementalBar('Playing games', max = iterations) as bar:
    for i in range(iterations):
        winner, scores = play_game()

        scores = [score for _, score in scores]

        winner_list.append(winner)
        score_list += scores

        if winner == -1:
            ties += 1

        bar.next()

bins = [i + 0.5 for i in range(-1, 5)]
plt.hist(winner_list, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore
print(f"Ties: {ties}")

plt.figure() #type: ignore
bins = [i + 0.5 for i in range(-1, max(score_list) + 1)]
plt.hist(score_list, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore
plt.show() #type: ignore