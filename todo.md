- 5 Players Game
- 3 Networks :
    - Choose Character
    - Choose between Money / District
    - Build District / Use Character


Players Money (5)            -     - Chosen Character (8)
Player Hand (54)             -
Players Hands Size (5)       -
Districts built (270)        -
Available Characters (5)     -
Unavailable Characters (2)   -


Players Money (5)            -     - Money / District (2)
Player Hand (54)             -
Players Hands Size (5)       -
Districts built (270)        -
Player Role (1)              -


Players Money (5)            -     - Player to use Character on (5)
Player Hand (54)             -     - District to build (54)
Players Hands Size (5)       -
Districts built (270)        -
Player Role (1)              -


# Game Cycle:
- Initialize
- Loop:
    - Select all characters
    - Play Rounds:
        - Get income
        - Argent/Quartier
        - Constuire Pouvoir
- Calculate points


# Optimizations:


Money: 0-30 number (31 numbers) -> 5 bits (32) * 5 : 25 bits
Role: 8 roles -> 3 bits * 5 : 15 bits
Head(24)-Money(25)-Role(15)=64 bits

Hands: 54 builds -> 54 bits * 5 : 270 bits
Player 0: Head(10)-Hands(54)=64 bits
Player 1: Head(10)-Hands(54)=64 bits
Player 2: Head(10)-Hands(54)=64 bits
Player 3: Head(10)-Hands(54)=64 bits
Player 4: Head(10)-Hands(54)=64 bits

Citadels: 54 builds -> 54 bits * 5 : 270 bits
Player 0: Head(10)-Citadels(54)=64 bits
Player 1: Head(10)-Citadels(54)=64 bits
Player 2: Head(10)-Citadels(54)=64 bits
Player 3: Head(10)-Citadels(54)=64 bits
Player 4: Head(10)-Citadels(54)=64 bits