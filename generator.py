import random
import math
from bitarray import bitarray


class permSolution():
    choice = None
    perm = None
    
    def __init__(self, choice, perm):
        self.choice = choice
        self.perm = perm
    
    def __str__(self) -> str:
        return f"{self.choice}, {self.perm}"

class matSolution():
    mat = None
    def __init__(self, matrix):
        self.mat = matrix
    
    def __str__(self) -> str:
        matStr = ""
        for row in self.mat:
            for el in row:
                matStr += str(el) + ' '
            matStr += '\n'
        return matStr
        
        
def distance(p1, p2):
    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )

def generateInitialSolutions(V, M, D, h, start_address, packs, amount=50):
    solutions = []
    sol_generated_count = 0
    generation_attempts_cout = 0
    
    while sol_generated_count <= amount:
        
        choice = bitarray(len(packs))
        choice.setall(0)
        for i, pack in enumerate(packs):  # Making sure that the packs with priority flag are selected
            if pack[4] == 1:
                choice[i] = 1
        packs_left_index = [i for i in range(len(packs)) if packs[i][4] == 0]

        # Random additional packs and random order
        additional_pack_count = random.randint(0, len(packs_left_index))

        for i in range(additional_pack_count):
            pack_nr = random.choice(packs_left_index)
            choice[pack_nr] = 1    
            packs_left_index.remove(pack_nr)
        
        chosen_packs = [pack for pack in packs if choice[pack[0]] == 1]

        perm = [pack[0] for pack in chosen_packs]
        random.shuffle(perm)

        # Checking if the solution is acceptable    
        dist = sum( [ distance(packs[perm[i]][3], packs[perm[i+1]][3]) for i in range(len(perm)-1) ] ) + distance(start_address, packs[perm[0]][3])
        count = choice.count(1)
        volume = sum( packs[perm[i]][2] for i in range(len(perm)) )
        weight = sum( packs[perm[i]][1] for i in range(len(perm)) )

        # Adding solution to the retured list if it is acceptable
        if dist <= D and count >= h and volume <= V and weight <= M:
            solutions.append( permSolution(choice, perm) )
            sol_generated_count += 1
        
        generation_attempts_cout += 1

    print(f"{generation_attempts_cout=}")
    return solutions

def solutionsToMatrices(solutions, packsCount):
    matrices = []
    for solution in solutions:
        matrix = [ bitarray(packsCount) for _ in range(packsCount)]
        for row in matrix:
            row.setall(0)
        for index, pack_nr in enumerate(solution.perm):
            matrix[pack_nr][index] = 1
        matrices.append(matSolution(matrix))
    return matrices
    



if __name__  == "__main__":

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

    # Prints package addresses map
    map = [['-' for _ in range(maxY)] for _ in range(maxX)]
    map[start_address[0]][start_address[1]] = 'X'
    for pack in packs:
        map[pack[3][0]][pack[3][1]] = '0'
    for row in map:
        for el in row:
            print(el, end=' ')
        print()

    # Generates and prints first batch of solutions
    print("\n\nFirst Generation:")
    solutions = generateInitialSolutions(V, M, D, h, start_address, packs, 20)
    solutionsMatrices = solutionsToMatrices(solutions, len(packs))
    for i in range(len(solutions)):
        print(solutions[i])
        print(solutionsMatrices[i])
