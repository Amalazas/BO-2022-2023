from simulation import *
from main import *
import sys
import os

CROSS_DICT = {
    "choice_from_one_order_from_other": choice_from_one_order_from_other,
    "extract_and_random_pick": extract_and_random_pick,
    "halve_and_swap": halve_and_swap,
    "random": None,
}
MUTATION_DICT = {
    "add_packs": add_packs,
    "cut_out_packs": cut_out_packs,
    "inverse_packages": inverse_packages,
    "inverse_permutation": inverse_permutation,
    "shift_block": shift_block,
    "shuffle_block": shuffle_block,
    "random": None,
}


if __name__ == "__main__":
    """ 
    Program arguments:

        problem_file_path,
        population_size,
        max_generations,
        max_iter_no_improvement, X
        alpha,
        crossover_rate, X
        mutation_rate,
        crossover_function,
        mutation_function,
        elitism_rate,
        crossover_max_attempts,
        mutation_max_attempts
        
        Example Run: py tester.py test_input_1.txt 1500 200 30 1.1 0.1 0.01 random random 0.2 10 10

        """
    
    if len(sys.argv) != 13:
        print("Please, provide all necessary arguments for this program - check source code for details")
        exit()

    # Reading and checking if the problem file is ok
    input = read_input_file("./input_files/" + sys.argv[1])
    if input is None:
        exit()
    
    # Creating the output file with descriptive name
    output_file_name = "test_output " \
                    + sys.argv[1]  + " " \
                    + sys.argv[2]  + " " \
                    + sys.argv[3]  + " " \
                    + sys.argv[4]  + " " \
                    + sys.argv[5]  + " " \
                    + sys.argv[6]  + " " \
                    + sys.argv[7]  + " " \
                    + sys.argv[8]  + " " \
                    + sys.argv[9]  + " " \
                    + sys.argv[10] + " " \
                    + sys.argv[11] + " " \
                    + sys.argv[12] + " " \
                    + ".txt"
    if not os.path.exists("./output"):
        os.makedirs("./output")
    
    with open("output/" + output_file_name, 'wt') as f:

        # Starting the simulation
        start_address, V, M, D, h, packs = input
        ga = GeneticAlgorithm(
            V, M, D, h,
            start_address,
            packs,
            population_size=int(sys.argv[2]),
            max_generations=int(sys.argv[3]),
            max_iter_no_improvement=int(sys.argv[4]),
            alpha=float(sys.argv[5]),
            crossover_rate=float(sys.argv[6]),
            mutation_rate=float(sys.argv[7]),
            crossover_function= CROSS_DICT[sys.argv[8]],
            mutation_function= MUTATION_DICT[sys.argv[9]],
            elitism_rate=float(sys.argv[10]),
            crossover_max_attempts=int(sys.argv[11]),
            mutation_max_attempts=int(sys.argv[12]),
            output_file = f
        )

        ga.run()
