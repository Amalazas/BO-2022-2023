import random
from typing import Any

from bitarray import bitarray

from generator import PermSolution


def inverse_permutation(perm: list[Any]) -> None:
    """Modifies a PermSolution by swapping unique pairs of
    permutation, ensuring distinct indices for each inversion.
    The number of swaps is a random integer from [1, len(perm) // 2]."""

    perm_len = len(perm)
    indices = [idx for idx in range(perm_len)]
    random.shuffle(indices)

    indices_set = set(indices)
    inverses_num = random.randint(1, perm_len // 2)
    for _ in range(inverses_num):
        i, j = indices_set.pop(), indices_set.pop()
        perm[i], perm[j] = perm[j], perm[i]


def shift_block(perm: list[Any]) -> None:
    """Randomly shifts a block of random length by a random number of positions within a permutation list."""

    if (perm_len := len(perm)) < 2:
        return None

    block_start_idx = random.randint(0, perm_len - 1)
    shift_block_len = random.randint(1, perm_len - 2)
    shift_block = perm[block_start_idx : block_start_idx + shift_block_len]

    if len(shift_block) != shift_block_len:
        end_shift_block_idx = shift_block_len - len(shift_block)
        rest_block = perm[end_shift_block_idx:block_start_idx]
        shift_block += perm[:end_shift_block_idx]
        insert_idx = 0
    else:
        rest_block = perm[:block_start_idx] + perm[block_start_idx + shift_block_len :]
        insert_idx = block_start_idx

    shift_postitions = random.randint(1, len(rest_block) - 1)
    insert_idx = (insert_idx + shift_postitions) % len(rest_block)
    perm = rest_block[:insert_idx] + shift_block + rest_block[insert_idx:]


def shuffle_block(perm: list[Any]) -> None:
    """Shuffles a randomly selected block of elements within a permutation list."""

    perm_len = len(perm)

    block_start_idx = random.randint(0, perm_len - 1)
    shuffle_block_len = random.randint(2, perm_len)
    shuffle_block = perm[block_start_idx : block_start_idx + shuffle_block_len]

    if len(shuffle_block) != shuffle_block_len:
        shuffle_block += perm[: shuffle_block_len - len(shuffle_block)]

    random.shuffle(shuffle_block)

    elems_to_end = len(perm) - block_start_idx
    perm[block_start_idx : block_start_idx + shuffle_block_len] = shuffle_block[
        :elems_to_end
    ]

    if elems_to_end < len(shuffle_block):
        perm[: len(shuffle_block) - elems_to_end] = shuffle_block[elems_to_end:]


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


if __name__ == "__main__":
    perm_sol = PermSolution(choice=bitarray("0011110101"), perm=[9, 2, 5, 3, 4, 7])

    print(perm_sol)
    # inverse_delivery_order(perm_sol)
    # shift_delivery_order_block(perm_sol)
    # shuffle_block(perm_sol.perm)
    inverse_packages(perm_sol)
    print(perm_sol)
