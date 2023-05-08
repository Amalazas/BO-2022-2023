from copy import copy
from random import uniform
from bitarray import bitarray

from generator import PermSolution, distance, generate_initial_solutions


def halve_and_swap(parent1: PermSolution, parent2: PermSolution, packs=None, V=None, M=None, D=None, h=None, start_address=None) -> PermSolution:
    """Dzielisz bitmapę na pół, wymieniasz je i uzupełniasz permutację kopiując fragmenty permutacji rodziców.
    Nie ma pewności, że potomek jest rozwiązaniem akceptowalnym!!!"""

    ## Childs' packages choice array
    half1 = parent1.choice[: len(parent1.choice) // 2]
    half2 = parent2.choice[len(parent2.choice) // 2 :]
    new_choice = half1 + half2

    ## Child's permutation
    new_perm = []
    # Going through the first half of the choice and getting subseries from parent1 permutation
    unused_packs_indexes = [i for i in range(len(half1)) if half1[i] == 1]

    while len(unused_packs_indexes) > 0:
        current_pack_nr = unused_packs_indexes.pop(0)
        new_perm.append(current_pack_nr)
        current_pack_nr_perm1_index = parent1.perm.index(current_pack_nr)
        while (
            current_pack_nr_perm1_index + 1
            < len(parent1.perm)  # Don't go beyond the size of permutation
            and (
                new_choice[parent1.perm[current_pack_nr_perm1_index + 1]] == 1
            )  # Add only packs selected for the child
            and parent1.perm[current_pack_nr_perm1_index + 1] not in new_perm
        ):  # Add only packs that are not already in the new_perm
            # Adding the next pack from the parent1 permutation to the child permutation
            current_pack_nr_perm1_index += 1
            if parent1.perm[current_pack_nr_perm1_index] in unused_packs_indexes:
                unused_packs_indexes.remove(parent1.perm[current_pack_nr_perm1_index])
            new_perm.append(parent1.perm[current_pack_nr_perm1_index])

    # Going through the second half of the choice and getting subseries from parent2 permutation
    unused_packs_indexes = [len(half1) + i for i in range(len(half2)) if half2[i] == 1]

    while len(unused_packs_indexes) > 0:
        current_pack_nr = unused_packs_indexes.pop(0)
        new_perm.append(current_pack_nr)
        current_pack_nr_perm2_index = parent2.perm.index(current_pack_nr)
        while (
            current_pack_nr_perm2_index + 1
            < len(parent2.perm)  # Don't go beyond the size of permutation
            and (
                new_choice[parent2.perm[current_pack_nr_perm2_index + 1]] == 1
            )  # Add only packs selected for the child
            and parent2.perm[current_pack_nr_perm2_index + 1] not in new_perm
        ):  # Add only packs that are not already in the new_perm
            # Adding the next pack from the parent2 permutation to the child permutation
            current_pack_nr_perm2_index += 1
            if parent2.perm[current_pack_nr_perm2_index] in unused_packs_indexes:
                unused_packs_indexes.remove(parent2.perm[current_pack_nr_perm2_index])
            new_perm.append(parent2.perm[current_pack_nr_perm2_index])

    return PermSolution(new_choice, new_perm)


def extract_and_random_pick(
    parent1: PermSolution, parent2: PermSolution, packs=None, V=None, M=None, D=None, h=None, start_address=None
) -> PermSolution:
    common_packages_bitmap = parent1.choice & parent2.choice
    new_perm = [
        package for package in parent2.perm if common_packages_bitmap[package] == 1
    ]
    left_packages = {
        package for package in parent2.perm if common_packages_bitmap[package] == 0
    } | {package for package in parent1.perm if common_packages_bitmap[package] == 0}

    v = m = d = 0
    for pckg_idx in new_perm:
        m += packs[pckg_idx][1]
        v += packs[pckg_idx][2]

    for i in range(len(new_perm) - 1):
        d += distance(packs[new_perm[i]][3], packs[new_perm[i + 1]][3])

    for pckg_idx in left_packages:
        _, pckg_m, pckg_v, (x, y), _ = packs[pckg_idx]
        if (
            v + pckg_v <= V
            and m + pckg_m <= M
            and d
            + distance(packs[new_perm[-1]][3], (x, y))
            + distance((x, y), packs[new_perm[0]][3])
            <= D
        ):
            new_perm.append(pckg_idx)

        v += pckg_v
        m += pckg_m
        d += distance(packs[new_perm[-1]][3], (x, y)) + distance(
            (x, y), packs[new_perm[0]][3]
        )
        # Random exit (trying to stop putting every package we can)
        if uniform(0,1) <= 0.33:
            break

    new_choice = bitarray(len(parent1.choice))
    new_choice.setall(0)
    for index in new_perm:
        new_choice[index] = 1

    return PermSolution(new_choice, new_perm)


def choice_from_one_order_from_other(
    parent1: PermSolution, parent2: PermSolution, packs=None, V=None, M=None, D=None, h=None, start_address=None
) -> PermSolution:
    """Copy choice of the first parent and base the order by the order of second parent.
    Nie ma pewności, że potomek jest rozwiązaniem akceptowalnym!!!
    Also, kinda weird way to cross :D"""

    new_choice = parent1.choice
    new_perm = []
    parent1_perm = copy(parent1.perm)
    parent2_perm = copy(parent2.perm)

    # Adding all the elements from parent1's perm in the order of parent2 to the child's permutation
    for pack in parent2_perm:
        if pack in parent1_perm:
            new_perm.append(pack)
            parent1_perm.remove(pack)

    # Inserting the packs picked only by the parent1 in order they were written in parent1's permutation
    for pack in parent1_perm:
        new_perm.insert(parent1.perm.index(pack), pack)

    return PermSolution(new_choice, new_perm)


if __name__ == "__main__":

    # EXAMPLE OF PROBLEM DEFINITION
    start_address = (0, 0)  # Starting point for the Courier
    max_x, max_y = 13, 20  # Map Dimentions

    V = 30  # Max Volume
    M = 30  # Max Weight
    D = 200  # Max Distance
    h = 5  # Min Number Of Chosen Packs

    packs = [
        (0, 2, 2, (3, 2), 0),
        (1, 2, 2, (1, 1), 0),
        (2, 10, 5, (10, 19), 1),
        (3, 4, 3, (10, 12), 0),
        (4, 2, 2, (3, 4), 1),
        (5, 1, 2, (1, 10), 0),
        (6, 12, 2, (4, 1), 0),
        (7, 2, 2, (12, 1), 1),
        (8, 5, 2, (9, 2), 0),
        (9, 3, 2, (5, 5), 0),
    ]

    # Generating and choosing solutions to cross
    solutions = generate_initial_solutions(V, M, D, h, start_address, packs, 20)
    parent1 = solutions[2]
    parent2 = solutions[15]
    print(f"Parent1: {parent1}\nParent2: {parent2}")
    child1_1 = halve_and_swap(parent1, parent2)
    child1_2 = halve_and_swap(parent2, parent1)
    child2_1 = extract_and_random_pick(parent1, parent2)
    child2_2 = extract_and_random_pick(parent2, parent1)
    child3_1 = choice_from_one_order_from_other(parent1, parent2)
    child3_2 = choice_from_one_order_from_other(parent2, parent1)
    print(
        f"Child1_1:  {child1_1}\nChild1_2:  {child1_2}\nChild2_1:  {child2_1}\nChild2_2:  {child2_2}\nChild3_1:  {child3_1}\nChild3_2:  {child3_2}"
    )
