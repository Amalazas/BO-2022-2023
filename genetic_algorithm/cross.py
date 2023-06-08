from copy import copy

from bitarray import bitarray
from generator import generate_initial_solutions
from data_classes import PermSolution, Point, Package


def halve_and_swap(
    parent1: PermSolution, parent2: PermSolution, *args, **kwargs
) -> PermSolution:
    """
    Dzielisz bitmapę na pół, wymieniasz je i uzupełniasz permutację kopiując fragmenty permutacji rodziców.
    Nie ma pewności, że potomek jest rozwiązaniem akceptowalnym!!!
    """

    # Child's choice array
    half1 = parent1.choice[: len(parent1.choice) // 2]
    half2 = parent2.choice[len(parent2.choice) // 2 :]
    new_choice = half1 + half2

    # Child's permutation
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
    parent1: PermSolution,
    parent2: PermSolution,
    packs: list[Package] = None,
    V: float = None,
    M: float = None,
    D: float = None,
    h: int = None,
    start_address: Point = None,
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
        m += packs[pckg_idx].weight
        v += packs[pckg_idx].volume

    for i in range(len(new_perm)):
        if i - 1 < 0:
            d += start_address.distance_to(packs[new_perm[i]].position)
        else:
            d += packs[new_perm[i - 1]].position.distance_to(
                packs[new_perm[i]].position
            )

    for pckg_idx in left_packages:
        _, pckg_m, pckg_v, pos, _ = packs[pckg_idx]

        last_point = packs[new_perm[-1]].position if new_perm else start_address

        new_dist = d + last_point.distance_to(pos) + pos.distance_to(start_address)
        if v + pckg_v <= V and m + pckg_m <= M and new_dist <= D:
            new_perm.append(pckg_idx)
            v += pckg_v
            m += pckg_m
            d = new_dist

    new_choice = bitarray(len(parent1.choice))
    new_choice.setall(0)
    for index in new_perm:
        new_choice[index] = 1

    return PermSolution(new_choice, new_perm)


def choice_from_one_order_from_other(
    parent1: PermSolution, parent2: PermSolution, *args, **kwargs
) -> PermSolution:
    """
    Copy choice of the first parent and base the order by the order of second parent.
    Nie ma pewności, że potomek jest rozwiązaniem akceptowalnym!!!
    Also, kinda weird way to cross :D
    """

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


CROSS_DICT = {
    "choice_from_one_order_from_other": choice_from_one_order_from_other,
    "extract_and_random_pick": extract_and_random_pick,
    "halve_and_swap": halve_and_swap,
    "random": None,
}


if __name__ == "__main__":
    # EXAMPLE OF PROBLEM DEFINITION
    start_address = Point(0, 0)  # Starting point for the Courier
    max_x, max_y = 13, 20  # Map Dimentions

    V = 30  # Max Volume
    M = 30  # Max Weight
    D = 200  # Max Distance
    h = 5  # Min Number Of Chosen Packs

    packs = [
        Package(0, 2, 2, Point(3, 2), 0),
        Package(1, 2, 2, Point(1, 1), 0),
        Package(2, 10, 5, Point(10, 19), 1),
        Package(3, 4, 3, Point(10, 12), 0),
        Package(4, 2, 2, Point(3, 4), 1),
        Package(5, 1, 2, Point(1, 10), 0),
        Package(6, 12, 2, Point(4, 1), 0),
        Package(7, 2, 2, Point(12, 1), 1),
        Package(8, 5, 2, Point(9, 2), 0),
        Package(9, 3, 2, Point(5, 5), 0),
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
