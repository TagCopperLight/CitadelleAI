#ifndef PLAYER_H
#define PLAYER_H

struct player{
    int id;
};

typedef struct player player;

player* player_init(int id);

void player_free(player* p);

#endif