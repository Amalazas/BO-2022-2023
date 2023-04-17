import random
import math
from generator import *
from bitarray import bitarray


def halveAndSwap(parent1: permSolution, parent2: permSolution) -> permSolution:
    """ Dzielisz bitmapę na pół, wymieniasz je i uzupełniasz permutację """
    
    print(parent1)
    print(parent2)
    half1 = parent1.choice[:len(parent1.choice)//2]
    half2 = parent2.choice[len(parent2.choice)//2:] 
    print(half1, half2)
    newChoice = half1 + half2
    
    # Do napisania: Tworzenie permutacji dla potomka.

    return None




if __name__ == "__main__":

    # EXAMPLE OF PROBLEM DEFINITION
    start_address = (0, 0)  # Starting point for the Courier
    maxX, maxY = 13, 20     # Map Dimentions

    V = 30   # Max Volume
    M = 30   # Max Weight
    D = 200  # Max Distance
    h = 5    # Min Number Of Chosen Packs

    packs = [
        (0,  2,  2, (3,2),   0),
        (1,  2,  2, (1,1),   0), 
        (2,  10, 5, (10,19), 1), 
        (3,  4,  3, (10,12), 0),
        (4,  2,  2, (3,4),   1),
        (5,  1,  2, (1,10),  0),
        (6,  12, 2, (4,1),   0),
        (7,  2,  2, (12,1),  1),
        (8,  5,  2, (9,2),   0),
        (9,  3,  2, (5,5),   0), 
    ]

    # Generating and choosing solutions to cross
    solutions = generateInitialSolutions(V, M, D, h, start_address, packs, 20)
    halveAndSwap(solutions[2], solutions[15])  # Just for testing purposes