import random
from typing import Any
from random import randint
from bitarray import bitarray

from generator import PermSolution


def inverse_permutation(individual: PermSolution) -> None:
    """Modifies a PermSolution by swapping unique pairs of
    permutation, ensuring distinct indices for each inversion.
    The number of swaps is a random integer from [1, len(perm) // 2]."""

    perm_len = len(individual.perm)
    indices = [idx for idx in range(perm_len)]
    random.shuffle(indices)

    indices_set = set(indices)
    inverses_num = random.randint(1, perm_len // 2)
    for _ in range(inverses_num):
        i, j = indices_set.pop(), indices_set.pop()
        individual.perm[i], individual.perm[j] = individual.perm[j], individual.perm[i]


def shift_block(individual: PermSolution) -> None:
    """Randomly shifts a block of random length by a random number of positions within a permutation list."""

    if (perm_len := len(individual.perm)) < 2:
        return None

    block_start_idx = random.randint(0, perm_len - 1)
    shift_block_len = random.randint(1, perm_len - 2)
    shift_block = individual.perm[block_start_idx : block_start_idx + shift_block_len]

    if len(shift_block) != shift_block_len:
        end_shift_block_idx = shift_block_len - len(shift_block)
        rest_block = individual.perm[end_shift_block_idx:block_start_idx]
        shift_block += individual.perm[:end_shift_block_idx]
        insert_idx = 0
    else:
        rest_block = individual.perm[:block_start_idx] + individual.perm[block_start_idx + shift_block_len :]
        insert_idx = block_start_idx

    shift_postitions = random.randint(1, len(rest_block) - 1)
    insert_idx = (insert_idx + shift_postitions) % len(rest_block)
    individual.perm = rest_block[:insert_idx] + shift_block + rest_block[insert_idx:]


def shuffle_block(individual: PermSolution) -> None:
    """Shuffles a randomly selected block of elements within a permutation list."""

    perm_len = len(individual.perm)

    block_start_idx = random.randint(0, perm_len - 1)
    shuffle_block_len = random.randint(2, perm_len)
    shuffle_block = individual.perm[block_start_idx : block_start_idx + shuffle_block_len]

    if len(shuffle_block) != shuffle_block_len:
        shuffle_block += individual.perm[: shuffle_block_len - len(shuffle_block)]

    random.shuffle(shuffle_block)

    elems_to_end = len(individual.perm) - block_start_idx
    individual.perm[block_start_idx : block_start_idx + shuffle_block_len] = shuffle_block[
        :elems_to_end
    ]

    if elems_to_end < len(shuffle_block):
        individual.perm[: len(shuffle_block) - elems_to_end] = shuffle_block[elems_to_end:]


def inverse_packages(individual: PermSolution) -> None:
    """Inverses random pair of (taken, nontaken) packages
    TODO: Implement in such a way that it is guaranteed not to produce invalid solutions???"""

    packages = individual.choice
    taken_packages = [i for i in range(len(packages)) if packages[i] == 1]
    nontaken_packages = [i for i in range(len(packages)) if packages[i] == 0]

    taken_package = random.choice(taken_packages)
    nontaken_package = random.choice(nontaken_packages)

    packages[taken_package] = 0
    packages[nontaken_package] = 1

    for i in range(len(individual.perm)):
        if individual.perm[i] == taken_package:
            individual.perm[i] = nontaken_package
            break


def cut_out_packs(individual: PermSolution) -> None:
    """ Cut out random number of packs from solution """
    nr_of_chosen_packs = 0
    chosen_indexes = []
    for index, bit in enumerate(individual.choice):
        if bit == 1:
            nr_of_chosen_packs += 1
            chosen_indexes.append(index)

    cut_off_ratio = 0.33  # How much do we want this to cut out off the gathered amount?
    nr_of_packs_to_cut = randint(0, round(nr_of_chosen_packs*cut_off_ratio))
    for _ in range(nr_of_packs_to_cut):
        index = random.choice(chosen_indexes)
        chosen_indexes.remove(index)
        individual.choice[index] = 0
        individual.perm.remove(index)
    


def add_packs(individual: PermSolution) -> None:
    """ Add random number of packs to the solution (place new pack into order randomly)"""
    not_chosen_indexes = []
    for index, bit in enumerate(individual.choice):
        if bit == 0:
            not_chosen_indexes.append(index)
    
    add_max_ratio = 0.20  # How much do we want to add at maximum?
    nr_of_packs_to_add = randint(0, round(len(individual.choice)*add_max_ratio))
    for _ in range(nr_of_packs_to_add):
        index = random.choice(not_chosen_indexes)
        not_chosen_indexes.remove(index)
        individual.choice[index] = 0
        individual.perm.insert(random.randint(0, len(individual.perm)), index)  # Adding the new package in the random place in the permutation


if __name__ == "__main__":
    perm_sol = PermSolution(choice=bitarray("0011110101"), perm=[9, 2, 5, 3, 4, 7])

    print(perm_sol)
    # inverse_delivery_order(perm_sol)
    # shift_delivery_order_block(perm_sol)
    # shuffle_block(perm_sol.perm)
    # inverse_packages(perm_sol)
    # cut_out_packs(perm_sol)
    add_packs(perm_sol)
    print(perm_sol)
