import random

from bitarray import bitarray
from data_classes import PermSolution, MatSolution, Point, Package


def generate_initial_solutions(V: float, M: float, D: float, h: int, start_address: Point, packs: list[Package], amount: int = 50,) -> list[PermSolution]:
    solutions = []
    sol_generated_count = 0
    generation_attempts_count = 0

    while sol_generated_count <= amount:
        print(f"Generated {sol_generated_count} out of {amount} initial solutions...", end="\r")

        choice = bitarray(len(packs))
        choice.setall(0)
        for i, pack in enumerate(packs):  # Making sure that the packs with priority flag are selected
            if pack.priority == 1:
                choice[i] = 1
        packs_left_index = [i for i in range(len(packs)) if packs[i].priority == 0]

        # Random additional packs and random order
        additional_pack_count = random.randint(0, len(packs_left_index))

        for i in range(additional_pack_count):
            pack_nr = random.choice(packs_left_index)
            choice[pack_nr] = 1
            packs_left_index.remove(pack_nr)

        chosen_packs = [pack for pack in packs if choice[pack.index] == 1]

        perm = [pack.index for pack in chosen_packs]
        random.shuffle(perm)

        # Checking if the solution is acceptable
        dist = sum(
            [
                packs[perm[i]].position.distance_to(packs[perm[i + 1]].position)
                for i in range(len(perm) - 1)
            ]
        ) + start_address.distance_to(packs[perm[0]].position)
        count = choice.count(1)
        volume = sum(packs[perm[i]].volume for i in range(len(perm)))
        weight = sum(packs[perm[i]].weight for i in range(len(perm)))

        # Adding solution to the retured list if it is acceptable
        if dist <= D and count >= h and volume <= V and weight <= M:
            solutions.append(PermSolution(choice, perm))
            sol_generated_count += 1

        generation_attempts_count += 1

    print("Done.")
    return solutions


def solutions_to_matrices(
    solutions: list[PermSolution], packs_count: int) -> list[MatSolution]:
    """Convert list of PermSolutions to a list of MatSolutions"""
    matrices = []
    for solution in solutions:
        matrix = [bitarray(packs_count) for _ in range(packs_count)]
        for row in matrix:
            row.setall(0)
        for index, pack_nr in enumerate(solution.perm):
            matrix[pack_nr][index] = 1
        matrices.append(MatSolution(matrix))
    return matrices


if __name__ == "__main__":
    # EXAMPLE OF PROBLEM DEFINITION
    start_address = Point(0, 0)  # Starting point for the Courier
    max_x, max_y = 30, 30  # Map Dimentions

    V = 100  # Max Volume
    M = 120  # Max Weight
    D = 180  # Max Distance
    h = 8  # Min Number Of Chosen Packs

    packs = [
        Package(0, 2, 1, Point(5, 25), 0),
        Package(1, 4, 8, Point(5, 1), 0),
        Package(2, 2, 10, Point(9, 15), 0),
        Package(3, 2, 7, Point(14, 13), 0),
        Package(4, 2, 2, Point(23, 29), 0),
        Package(5, 2, 8, Point(23, 14), 0),
        Package(6, 8, 7, Point(21, 17), 1),
        Package(7, 4, 5, Point(28, 27), 0),
        Package(8, 1, 3, Point(2, 14), 0),
        Package(9, 3, 7, Point(20, 5), 0),
        Package(10, 4, 1, Point(7, 7), 0),
        Package(11, 5, 1, Point(16, 26), 0),
        Package(12, 8, 6, Point(17, 29), 0),
        Package(13, 1, 1, Point(25, 21), 1),
        Package(14, 5, 7, Point(29, 17), 0),
        Package(15, 3, 1, Point(7, 9), 0),
        Package(16, 5, 3, Point(23, 4), 0),
        Package(17, 3, 8, Point(9, 23), 0),
        Package(18, 8, 6, Point(28, 7), 0),
        Package(19, 8, 9, Point(7, 29), 0),
        Package(20, 8, 1, Point(9, 15), 0),
        Package(21, 3, 1, Point(2, 24), 0),
        Package(22, 7, 8, Point(27, 27), 0),
        Package(23, 8, 1, Point(5, 12), 0),
        Package(24, 1, 4, Point(13, 2), 0),
        Package(25, 6, 4, Point(6, 15), 1),
        Package(26, 4, 6, Point(16, 7), 0),
        Package(27, 4, 2, Point(28, 18), 0),
        Package(28, 2, 5, Point(15, 17), 0),
        Package(29, 5, 1, Point(16, 9), 0),
    ]

    # Prints package addresses map
    map = [["-" for _ in range(max_y)] for _ in range(max_x)]
    map[start_address.x][start_address.y] = "X"
    for pack in packs:
        map[pack.position.x][pack.position.y] = pack.index
    for row in map:
        for el in row:
            print(el, end=" ")
        print()

    # Generates and prints first batch of solutions
    # print("\n\nFirst Generation:")
    # solutions = generate_initial_solutions(V, M, D, h, start_address, packs, 20)
    # solutions_matrices = solutions_to_matrices(solutions, len(packs))
    # for i in range(len(solutions)):
    #     print(solutions[i])
    #     print(solutions_matrices[i])
