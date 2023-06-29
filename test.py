from game import Game
from data import ROLES, DISTRICTS
from player import Player

from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.plotting import figure


def play_game() -> int:
    players = [Player(0), Player(1), Player(2), Player(3), Player(4)]

    game = Game(players, ROLES, DISTRICTS)
    game.init()

    turn = 0

    while True:
        game.select_characters()
        game.play()

        if game.game_over()[0]:
            return game.game_over()[1].id

        turn += 1

players = ['0', '1', '2', '3', '4']
counts = [0, 0, 0, 0, 0]

source = ColumnDataSource(data=dict(players=players, counts=counts))
fig = figure(x_range=players)
fig.vbar(x='players', top='counts', width=0.8, source=source)

def update_chart():
    new_data = source.data["counts"]
    new_data[play_game()] += 1
    source.data["counts"] = new_data

curdoc().add_root(fig)
curdoc().add_periodic_callback(update_chart, 1)