import simulation
import sys
import os
from data_classes import Point, Package

def read_input_file(path: str):

    if not os.path.exists(path):
        print("Input file does not exist!")
        return None

    with open(path, 'r') as f_input:
        Lines = f_input.readlines()
        
        start_address = Point(*map(int, Lines.pop(0).split()))
        V, M, D, h = Lines.pop(0).split()
        
        packs = []
        for line in Lines:
            index, weight, volume, x, y, priority = line.split()
            pack = Package(int(index), float(weight), float(volume), Point(float(x), float(y)), int(priority))
            packs.append(pack)
    
    if packs is not None:
        return start_address, V, M, D, h, packs
    
    else:
        print("Error while loading the input file!")
        return None


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Please, provide the input file's name with extention as an argument!")
        exit()

    input = read_input_file("./input/" + sys.argv[1])
    
    if input is None:
        exit()

    start_address, V, M, D, h, packs = input    

    ga = simulation.GeneticAlgorithm(
        V, M, D, h,
        start_address,
        packs,
        population_size=1500,
        max_generations=200,
        mutation_rate=0.01,
        elitism_rate=0.10,
        crossover_max_attempts=10,
        mutation_max_attempts=10,
        alpha=2,
    )

    ga.run()
    print(f"Last Population's best individual:\n{ga.best_individual}")
    ga.display_solution(ga.best_individual.perm)