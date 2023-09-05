#ifndef GAME_H
#define GAME_H

#include <string.h>

#include "player.h"
#include "district.h"

struct game{
    player** players;
    int** districts_data;

    int* districts;
    int bank;
    int crown;

    int* moneys;
    int* roles;

    int** hands;
    int** citadels;
    int* citadels_size;

    int first_to_finish;

    bool debug;
};

typedef struct game game;

game* game_init(player** players, int** districts_data, bool debug);

int* get_select_order(game* game);
void select_characters(game* game);
void play(game* game);
void calculate_incomes(game* game, player* player, int color);
int** calculate_scores(game* game);
int* game_over(game* game);
char* repr(game* game);

void game_free(game* game);

#endif