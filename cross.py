import random
import math
from generator import *
from bitarray import bitarray


def halveAndSwap(parent1: permSolution, parent2: permSolution) -> permSolution:  # NOT FINISHED
    """ Dzielisz bitmapę na pół, wymieniasz je i uzupełniasz permutację """
    
    print(parent1)
    print(parent2)
    half1 = parent1.choice[:len(parent1.choice)//2]
    half2 = parent2.choice[len(parent2.choice)//2:] 
    print(half1, half2)
    newChoice = half1 + half2
    
    # Do napisania: Tworzenie permutacji dla potomka.
    

    return None


def extract_and_random_pick(parent1: permSolution, parent2: permSolution) -> permSolution:
    common_packages_bitmap = parent1.choice & parent2.choice
    
    print(parent1)
    print(parent2)

    new_perm = [package for package in parent2.perm if common_packages_bitmap[package] == 1]
    left_packages = {package for package in parent2.perm if common_packages_bitmap[package] == 0} | {package for package in parent1.perm if common_packages_bitmap[package] == 0}
    
    v = m = d = 0
    for pckg_idx in new_perm:
        pckg = packs[pckg_idx]
        m += packs[pckg_idx][1]
        v += packs[pckg_idx][2]

    for i in range(len(new_perm) - 1):
        d += distance(packs[new_perm[i]][3], packs[new_perm[i + 1]][3])
    
    for pckg_idx in left_packages:
        _, pckg_m, pckg_v, (x, y), _ = packs[pckg_idx]
        if v + pckg_v <= V and m + pckg_m <= M and d + distance(packs[new_perm[-1]][3], (x, y)) + distance((x, y), packs[new_perm[0]][3]) <= D:
            new_perm.append(pckg_idx)
        
        v += pckg_v
        m += pckg_m
        d += distance(packs[new_perm[-1]][3], (x, y)) + distance((x, y), packs[new_perm[0]][3])

    new_choice = bitarray(len(parent1.choice))
    new_choice.setall(0)
    for index in new_perm:
        new_choice[index] = 1

    return permSolution(new_choice, new_perm)




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
    # print(extract_and_random_pick(solutions[2], solutions[15]))
