from cross import *
from mutation import *
from generator import *
from simulation import *
from random import uniform


def generate_packs(max_x, max_y, V, M, count):
    packs = []

    max_pack_volume = 3 * V // count
    max_pack_mass = 3 * M // count

    for i in range(count):
        pack = (
            i,
            randint(1, max_pack_mass),
            randint(1, max_pack_volume),
            (randint(0, max_x - 1), randint(0, max_y - 1)),
            1 if (uniform(0, 1) < 0.20) else 0,
        )
        packs.append(pack)

    return packs


if __name__ == "__main__":
    # TEST GENERATOR
    start_address = (15, 15)  # Starting point for the Courier
    max_x, max_y = 30, 30  # Map Dimentions

    V = 300  # Max Volume
    M = 300  # Max Weight
    D = 120  # Max Distance
    h = 10  # Min Number Of Chosen Packs

    packs = generate_packs(max_x, max_y, V, M, 20)

    # Prints package addresses map
    map = [["-" for _ in range(max_y)] for _ in range(max_x)]
    map[start_address[0]][start_address[1]] = "X"
    for pack in packs:
        map[pack[3][0]][pack[3][1]] = pack[0]
    for row in map:
        for el in row:
            print(el, end=" ")
        print()

    # Prints generated test (input)
    print("\n\n")
    print(f"{start_address[0]} {start_address[0]}")
    print(f"{V} {M} {D} {h}")
    for pack in packs:
        print(f"{pack[0]} {pack[1]} {pack[2]} {pack[3][0]} {pack[3][1]} {pack[4]}")
