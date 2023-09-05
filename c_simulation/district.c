#include <stdlib.h>

#include "district.h"

int** get_districts_data(){
    int** district_data = malloc(sizeof(int*) * 54);
    for(int i = 0; i < 54; i++){
        district_data[i] = malloc(sizeof(int) * 2);
    }
    district_data[0][0] = 1; district_data[0][1] = 2;
    district_data[1][0] = 1; district_data[1][1] = 2;
    district_data[2][0] = 1; district_data[2][1] = 2;
    district_data[3][0] = 2; district_data[3][1] = 2;
    district_data[4][0] = 2; district_data[4][1] = 2;
    district_data[5][0] = 2; district_data[5][1] = 2;
    district_data[6][0] = 3; district_data[6][1] = 2;
    district_data[7][0] = 3; district_data[7][1] = 2;
    district_data[8][0] = 3; district_data[8][1] = 2;
    district_data[9][0] = 5; district_data[9][1] = 2;
    district_data[10][0] = 5; district_data[10][1] = 2;
    district_data[11][0] = 1; district_data[11][1] = 4;
    district_data[12][0] = 1; district_data[12][1] = 4;
    district_data[13][0] = 1; district_data[13][1] = 4;
    district_data[14][0] = 2; district_data[14][1] = 4;
    district_data[15][0] = 2; district_data[15][1] = 4;
    district_data[16][0] = 2; district_data[16][1] = 4;
    district_data[17][0] = 3; district_data[17][1] = 4;
    district_data[18][0] = 3; district_data[18][1] = 4;
    district_data[19][0] = 3; district_data[19][1] = 4;
    district_data[20][0] = 5; district_data[20][1] = 4;
    district_data[21][0] = 5; district_data[21][1] = 4;
    district_data[22][0] = 3; district_data[22][1] = 1;
    district_data[23][0] = 3; district_data[23][1] = 1;
    district_data[24][0] = 3; district_data[24][1] = 1;
    district_data[25][0] = 3; district_data[25][1] = 1;
    district_data[26][0] = 3; district_data[26][1] = 1;
    district_data[27][0] = 4; district_data[27][1] = 1;
    district_data[28][0] = 4; district_data[28][1] = 1;
    district_data[29][0] = 4; district_data[29][1] = 1;
    district_data[30][0] = 4; district_data[30][1] = 1;
    district_data[31][0] = 5; district_data[31][1] = 1;
    district_data[32][0] = 5; district_data[32][1] = 1;
    district_data[33][0] = 5; district_data[33][1] = 1;
    district_data[34][0] = 1; district_data[34][1] = 3;
    district_data[35][0] = 1; district_data[35][1] = 3;
    district_data[36][0] = 1; district_data[36][1] = 3;
    district_data[37][0] = 1; district_data[37][1] = 3;
    district_data[38][0] = 1; district_data[38][1] = 3;
    district_data[39][0] = 2; district_data[39][1] = 3;
    district_data[40][0] = 2; district_data[40][1] = 3;
    district_data[41][0] = 2; district_data[41][1] = 3;
    district_data[42][0] = 2; district_data[42][1] = 3;
    district_data[43][0] = 2; district_data[43][1] = 3;
    district_data[44][0] = 2; district_data[44][1] = 3;
    district_data[45][0] = 2; district_data[45][1] = 3;
    district_data[46][0] = 3; district_data[46][1] = 3;
    district_data[47][0] = 3; district_data[47][1] = 3;
    district_data[48][0] = 3; district_data[48][1] = 3;
    district_data[49][0] = 4; district_data[49][1] = 3;
    district_data[50][0] = 4; district_data[50][1] = 3;
    district_data[51][0] = 4; district_data[51][1] = 3;
    district_data[52][0] = 5; district_data[52][1] = 3;
    district_data[53][0] = 5; district_data[53][1] = 3;

    return district_data;
}

void free_districts_data(int** district_data){
    for(int i = 0; i < 54; i++){
        free(district_data[i]);
    }
    free(district_data);
}