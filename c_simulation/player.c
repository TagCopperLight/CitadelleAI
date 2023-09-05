#include <stdlib.h>

#include "player.h"

player* player_init(int id){
    player* p = malloc(sizeof(player));
    p->id = id;
    return p;
}

void player_free(player* p){
    free(p);
}