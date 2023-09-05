#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "game.h"

game* game_init(player** players, int** districts_data, bool debug){
    game* self = (game*)malloc(sizeof(game));

    self->players = players;
    self->districts_data = districts_data;

    self->districts = (int*)malloc(sizeof(int) * 54);
    self->bank = 30 - (5 * 2);
    self->crown = 0; //TODO: randomize crown position
    
    self->moneys = (int*)malloc(sizeof(int) * 5);
    for(int i = 0; i < 5; i++){
        self->moneys[i] = 2;
    }

    self->roles = (int*)malloc(sizeof(int) * 5);
    for(int i = 0; i < 5; i++){
        self->roles[i] = -1;
    }

    self->hands = (int**)malloc(sizeof(int*) * 5);
    for(int i = 0; i < 5; i++){
        self->hands[i] = (int*)malloc(sizeof(int) * 54);
    }

    self->citadels = (int**)malloc(sizeof(int*) * 5);
    for(int i = 0; i < 5; i++){
        self->citadels[i] = (int*)malloc(sizeof(int) * 54);
    }

    self->citadels_size = (int*)malloc(sizeof(int) * 5);
    for(int i = 0; i < 5; i++){
        self->citadels_size[i] = 0;
    }

    self->first_to_finish = -1;

    self->debug = debug;

    

    return self;
}