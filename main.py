from simulation.game import Game
from optimized_simulation.ogame import OGame
from simulation.data import ODISTRICTS, ROLES, DISTRICTS
from simulation.player.player import Player
from optimized_simulation.player.oplayer import OPlayer

import time
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm

from multiprocessing import Pool, current_process


def debug(*args: str|int|OGame|Game) -> None:
    if DEBUG:
        print(*args)

def graph(winner_list : list[int], score_list: list[int], turn_list: list[int], show: bool) -> None:
    total_games = len(winner_list)
    print(f"Total games: {total_games}")
    print(f"Games/second: {total_games / (time.time() - start_time)}")
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


def play_game() -> tuple[int, list[int], int]:
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
            scores = [score for _, score in game.calculate_scores()]
            return game.game_over()[1].id, scores, turn

        turn += 1

def oplay_game() -> tuple[int, list[int], int]:
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
            scores = [score for _, score in game.calculate_scores()]
            return game.game_over()[1], scores, turn

        turn += 1

def process(iterations: int, o: bool) -> tuple[list[int], list[int], list[int]]:
    winner_list: list[int] = []
    score_list: list[int] = []
    turn_list: list[int] = []

    process_id = current_process()._identity[0]

    if BAR and (process_id == 1 or process_id == 7):
        for _ in tqdm(range(iterations)):
            winner, scores, turns = play_game() if not o else oplay_game()

            winner_list.append(winner)
            turn_list.append(turns)
            score_list += scores
    else:
        for _ in range(iterations):
            winner, scores, turns = play_game() if not o else oplay_game()

            winner_list.append(winner)
            turn_list.append(turns)
            score_list += scores

    return winner_list, score_list, turn_list

def worker(iterations_o: tuple[int, bool]) -> tuple[list[int], list[int], list[int]]:
    iterations, o = iterations_o
    p = process(iterations, o)
    return p

def main(iterations:int, processes:int, o: bool) -> None:
    with Pool(processes=processes) as pool: #type: ignore
        results = pool.map(worker, [(iterations//processes, o) for _ in range(processes)], chunksize=1)
        results += pool.map(worker, [(iterations%processes, o)], chunksize=1)
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
GRAPHS = True

start_time = time.time()
main(100000, 6, True)