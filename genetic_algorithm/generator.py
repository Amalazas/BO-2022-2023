import math
import random

from bitarray import bitarray


class PermSolution():
    choice = None
    perm = None
    age = 0
    
    def __init__(self, choice, perm) -> None:
        self.choice = choice
        self.perm = perm
    
    def __str__(self) -> str:
        return f"{self.choice}, {self.perm}"

class MatSolution():
    mat = None
    
    def __init__(self, matrix):
        self.mat = matrix
    
    def __str__(self) -> str:
        mat_str = ""
        for row in self.mat:
            for el in row:
                mat_str += str(el) + ' '
            mat_str += '\n'
        return mat_str
        
        
def distance(p1, p2):
    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )

def generate_initial_solutions(V, M, D, h, start_address, packs, amount=50):
    solutions = []
    sol_generated_count = 0
    generation_attempts_count = 0
    updated_at = 0
    updated = False

    while sol_generated_count <= amount:
        
        # Printing updates on the initial soultion generation
        if sol_generated_count >= 0.8 * amount and updated_at < 0.8:
            updated_at = 0.8
            updated = True
        elif sol_generated_count >= 0.6 * amount and updated_at < 0.6:
            updated_at = 0.6
            updated = True
        elif sol_generated_count >= 0.4 * amount and updated_at < 0.4:
            updated_at = 0.4
            updated = True
        elif sol_generated_count >= 0.2 * amount and updated_at < 0.2:
            updated_at = 0.2
            updated = True
        if updated:
            print(f"Generated {updated_at * 100}% of initial population...")
            updated = False

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
            solutions.append( PermSolution(choice, perm) )
            sol_generated_count += 1
        
        generation_attempts_count += 1

    # print(f"{generation_attempts_count=}")
    return solutions

def solutions_to_matrices(solutions, packsCount):
    """ Convert list of PermSolutions to a list of MatSolutions """
    matrices = []
    for solution in solutions:
        matrix = [ bitarray(packsCount) for _ in range(packsCount)]
        for row in matrix:
            row.setall(0)
        for index, pack_nr in enumerate(solution.perm):
            matrix[pack_nr][index] = 1
        matrices.append(MatSolution(matrix))
    return matrices
    



if __name__  == "__main__":

    # EXAMPLE OF PROBLEM DEFINITION
    start_address = (0, 0)  # Starting point for the Courier
    max_x, max_y = 30, 30     # Map Dimentions

    V = 100   # Max Volume
    M = 120   # Max Weight
    D = 180  # Max Distance
    h = 8    # Min Number Of Chosen Packs

    packs = [
        (0, 2, 1, (5, 25), 0),
        (1, 4, 8, (5, 1), 0),
        (2, 2, 10, (9, 15), 0),
        (3, 2, 7, (14, 13), 0),
        (4, 2, 2, (23, 29), 0),
        (5, 2, 8, (23, 14), 0),
        (6, 8, 7, (21, 17), 1),
        (7, 4, 5, (28, 27), 0),
        (8, 1, 3, (2, 14), 0),
        (9, 3, 7, (20, 5), 0),
        (10, 4, 1, (7, 7), 0),
        (11, 5, 1, (16, 26), 0),
        (12, 8, 6, (17, 29), 0),
        (13, 1, 1, (25, 21), 1),
        (14, 5, 7, (29, 17), 0),
        (15, 3, 1, (7, 9), 0),
        (16, 5, 3, (23, 4), 0),
        (17, 3, 8, (9, 23), 0),
        (18, 8, 6, (28, 7), 0),
        (19, 8, 9, (7, 29), 0),
        (20, 8, 1, (9, 15), 0),
        (21, 3, 1, (2, 24), 0),
        (22, 7, 8, (27, 27), 0),
        (23, 8, 1, (5, 12), 0),
        (24, 1, 4, (13, 2), 0),
        (25, 6, 4, (6, 15), 1),
        (26, 4, 6, (16, 7), 0),
        (27, 4, 2, (28, 18), 0),
        (28, 2, 5, (15, 17), 0),
        (29, 5, 1, (16, 9), 0),
    ]

    # Prints package addresses map
    map = [['-' for _ in range(max_y)] for _ in range(max_x)]
    map[start_address[0]][start_address[1]] = 'X'
    for pack in packs:
        map[pack[3][0]][pack[3][1]] = pack[0]
    for row in map:
        for el in row:
            print(el, end=' ')
        print()

    # Generates and prints first batch of solutions
    # print("\n\nFirst Generation:")
    # solutions = generate_initial_solutions(V, M, D, h, start_address, packs, 20)
    # solutions_matrices = solutions_to_matrices(solutions, len(packs))
    # for i in range(len(solutions)):
    #     print(solutions[i])
    #     print(solutions_matrices[i])
