from simulation.game import Game
from simulation.data import ROLES, DISTRICTS
from simulation.player.player import Player
from simulation.player.basic_player import BasicPlayer #type: ignore

import time
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm

from multiprocessing import Pool, current_process


def debug(*args: str|int|Game) -> None:
    if DEBUG:
        print(*args)

def graph(winner_list : list[int], score_list: list[int], turn_list: list[int], show: bool) -> tuple[int, float]:
    total_games = len(winner_list)
    print(f"Total games: {total_games}")
    duration = time.time() - start_time
    print(f"Games/second: {total_games / duration}")
    turn_array = np.array(turn_list)
    print(f"Average turns: {np.mean(turn_array)}")
    print("--- %s seconds ---" % (time.time() - start_time), "\n")

    if show:
        bins = [i + 0.5 for i in range(-1, 5)]
        plt.hist(winner_list, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore

        plt.figure() #type: ignore
        bins = [i + 0.5 for i in range(-1, max(score_list) + 1)]
        plt.hist(score_list, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore
        plt.show() #type: ignore

    return total_games, duration


def play_game() -> tuple[int, list[tuple[Player, int]], int]:
    players: list[Player] = [Player(0)] + [Player(i) for i in range(1, 5)]

    game = Game(players, ROLES, DISTRICTS, DEBUG)
    game.init()
    debug(game, "\n")

    turn = 0

    while True:
        debug("----------- Turn", turn, "----------- \n")
        game.select_characters()
        game.play()
        debug("")
        debug(game, "\n")

        if game.game_over()[0]:
            return game.game_over()[1].id, game.calculate_scores(), turn

        turn += 1


def process(iterations: int) -> tuple[list[int], list[int], list[int]]:
    winner_list: list[int] = []
    score_list: list[int] = []
    turn_list: list[int] = []

    process_id = current_process()._identity[0]

    if BAR and process_id == 1:
        for _ in tqdm(range(iterations)):
            winner, scores, turns = play_game()

            scores = [score for _, score in scores]

            winner_list.append(winner)
            turn_list.append(turns)
            score_list += scores
    else:
        for _ in range(iterations):
            winner, scores, turns = play_game()

            scores = [score for _, score in scores]

            winner_list.append(winner)
            turn_list.append(turns)
            score_list += scores

    return winner_list, score_list, turn_list

def worker(iterations: int) -> tuple[list[int], list[int], list[int]]:
    p = process(iterations)
    return p

def main(iterations:int, processes:int) -> tuple[int, float]:
    with Pool(processes=processes) as pool: #type: ignore
        results = pool.map(worker, [iterations//processes for _ in range(processes)], chunksize=1)
        results += pool.map(worker, [iterations%processes], chunksize=1)
        pool.close()

    winner_list: list[int] = []
    score_list: list[int] = []
    turn_list: list[int] = []

    for result in results:
        winner_list += result[0]
        score_list += result[1]
        turn_list += result[2]

    return graph(winner_list, score_list, turn_list, GRAPHS)


DEBUG = False
BAR = False
GRAPHS = False

ITERATIONS = 10000
game_list: list[list[int]] = []
duration_list: list[list[float]] = []

for i in range(1, 17):
    game_list.append([])
    duration_list.append([])
    for _ in range(20):
        print(f"Running {ITERATIONS} games with {i} processes (iteration {_}))")
        start_time = time.time()
        games, durations = main(ITERATIONS, i)

        game_list[i-1].append(games)
        duration_list[i-1].append(durations)

game_array = np.array(game_list)
duration_array = np.array(duration_list)
games_seconds = game_array / duration_array
means = np.mean(games_seconds, axis=1)
stds = np.std(games_seconds, axis=1, ddof=1)

plt.figure() #type: ignore
plt.plot(range(1, 17), means, label="Mean") #type: ignore
plt.plot(range(1, 17), means + stds, label="Mean + 1 std") #type: ignore
plt.plot(range(1, 17), means - stds, label="Mean - 1 std") #type: ignore
plt.show() #type: ignore