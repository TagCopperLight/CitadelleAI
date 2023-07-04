from optimized_simulation.ogame import OGame
from simulation.data import ODISTRICTS
from optimized_simulation.player.oplayer import OPlayer

import time
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm

import cProfile
import pstats

from multiprocessing import Pool, current_process


def debug(*args: str|int|OGame) -> None:
    if DEBUG:
        print(*args)

def graph(winner_list : list[int], score_list: list[int], turn_list: list[int], show: bool) -> None:
    total_games = len(winner_list)
    print(f"Total games: {total_games}")
    print(f"Games/second: {total_games / (time.time() - start_time)}")
    turn_array = np.array(turn_list)
    print(f"Average turns: {np.mean(turn_array)}")

    bins = [i + 0.5 for i in range(-1, 5)]
    plt.hist(winner_list, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore

    plt.figure() #type: ignore
    bins = [i + 0.5 for i in range(-1, max(score_list) + 1)]
    plt.hist(score_list, bins = bins, edgecolor = 'black', histtype = 'bar') #type: ignore
    print("--- %s seconds ---" % (time.time() - start_time), "\n")
    if show:
        plt.show() #type: ignore


def play_game() -> tuple[int, list[tuple[int, int]], int]:
    players: list[OPlayer] = [OPlayer(0)] + [OPlayer(i) for i in range(1, 5)]

    game = OGame(players, ODISTRICTS, DEBUG)
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
            return game.game_over()[1], game.calculate_scores(), turn

        turn += 1

def process(iterations: int) -> tuple[list[int], list[int], list[int]]:
    winner_list: list[int] = []
    score_list: list[int] = []
    turn_list: list[int] = []

    # process_id = current_process()._identity[0]

    # if BAR and process_id == 1:
    if BAR:
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

def main(iterations:int, processes:int) -> None:
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

    graph(winner_list, score_list, turn_list, GRAPHS)


DEBUG = False
BAR = True
GRAPHS = False

start_time = time.time()
# main(100000, 6)
cProfile.run('process(10000)', 'restats')
p = pstats.Stats('restats')
p.sort_stats('cumulative').print_stats(20)