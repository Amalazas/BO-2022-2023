import random
import matplotlib.pyplot as plt

from generator import PermSolution
from generator import generate_initial_solutions, distance
from cross import halve_and_swap, choice_from_one_order_from_other, extract_and_random_pick
from mutation import inverse_permutation, shift_block, shuffle_block, inverse_packages, add_packs, cut_out_packs

class GeneticAlgorithm:
    """
    Genetic algorithm for solving the problem of choosing packages to be delivered.
    Constants:
        max_volume: maximum volume of the packages that can be chosen
        max_weight: maximum weight of the packages that can be chosen
        max_distance: maximum distance that can be travelled
        min_chosen_packs: minimum number of chosen packages
        start_address: starting address of the courier
        packs: list of packages
    Parameters:
        population_size: size of the population
        max_generations: maximum number of generations (iterations)
        alpha: parameter of the objective function
        mutation_rate: probability of mutation
        crossover_function: function used for crossover
        mutation_function: function used for mutation
        elitism_rate: rate of elitism (percentage of best individuals that are selected for crossover)
        crossover_max_attempts: maximum number of attempts of crossover (if crossover returns invalid solution then it is repeated)
        mutation_max_attempts: maximum number of attempts of mutation (if mutation returns invalid solution then it is repeated)
        log_every: number of generations after which informations are printed
    """
    def __init__(self, max_volume, max_weight, max_distance, min_chosen_packs, start_address, packs, population_size=100,
                  max_generations=1000, alpha=1.15, mutation_rate=0.005, crossover_function=None, mutation_function=None, elitism_rate=0.1,
                  crossover_max_attempts=1000, mutation_max_attempts=1000, log_every=1):
        self.population = []
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.max_distance = max_distance
        self.min_chosen_packs = min_chosen_packs
        self.start_address = start_address
        self.packs = packs
        # for simplicity population_size is even
        self.population_size = population_size if population_size % 2 == 0 else population_size + 1
        self.max_generations = max_generations
        self.alpha = alpha
        self.crossover_function = crossover_function
        self.mutation_function = mutation_function
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        self.crossover_max_attempts = crossover_max_attempts
        self.mutation_max_attempts = mutation_max_attempts
        self.log_every = log_every
        self.best_score = float('inf')
        self.best_individual = None
        self.scores = []
        self.priority_packs_indexes = (pack[0] for pack in packs if pack[4] != 0)

    def run(self):
        """Runs the genetic algorithm."""
        self._initialize_population()
        for i in range(self.max_generations):
            if i % self.log_every == 0:
                print(f"Generation {i: <{len(str(self.max_generations))}} | Best score: {self.best_score: < 20} | Current generation best score: {self._fitness(self.population[0])}")
            # for individual in self.population:
            #     print(f"{individual.perm} | {self._fitness(individual)}")
            # Selection
            selected_parents = self._select()
            # Crossover
            crossed_children = self._crossover(selected_parents)
            # Mutation
            self._mutate(crossed_children)
            # Replacement
            self._replace(crossed_children)

    def _initialize_population(self) -> None:
        """Generates initial population of size 'population_size.'"""
        print("Initializing population...")
        self.population = sorted(generate_initial_solutions(self.max_volume, self.max_weight, self.max_distance, self.min_chosen_packs, self.start_address, self.packs, self.population_size), key=self._fitness)
        self.best_individual = self.population[0]
        self.best_score = self._fitness(self.best_individual)
        print("Population initialized.")
    
    def _verify(self, individual: PermSolution) -> bool:
        """Verifies if the individual is valid. Returns True if the individual is valid, False otherwise."""
        seen = set()
        for i in individual.perm:
            if i in seen:
                return False
            seen.add(i)
        for i in self.priority_packs_indexes:
            if individual.choice[i] == 0:
                return False
        if len(individual.perm) < self.min_chosen_packs:
            return False
        if sum(self.packs[i][1] for i in individual.perm) > self.max_weight:
            return False
        if sum(self.packs[i][2] for i in individual.perm) > self.max_volume:
            return False
        if sum(distance(self.packs[individual.perm[i]][3], self.packs[individual.perm[i + 1]][3]) for i in range(len(individual.perm) - 1)) + distance(self.start_address, self.packs[individual.perm[0]][3]) > self.max_distance:
            return False
        return True

    def _fitness(self, individual: PermSolution) -> float:
        """Returns the fitness of the individual. The lower the better. Implemetation of objective function from presentation. For permutations of length 0 returns infinity."""
        score = float('inf')
        if len(individual.perm) != 0:
            total_weight = sum(self.packs[i][1] for i in individual.perm)
            score = total_weight * distance(self.start_address, self.packs[individual.perm[0]][3])
            total_weight -= self.packs[individual.perm[0]][1]
            for i in range(1, len(individual.perm)):
                score += total_weight * distance(self.packs[individual.perm[i-1]][3], self.packs[individual.perm[i]][3])
                total_weight -= self.packs[individual.perm[i]][1]
            total_weight /= self.alpha ** len(individual.perm)
        return score

    def _select(self):
        """Selects individuals for crossover. Mixed elitisim and roulette wheel selection. Returns a list of selected parents."""
        elitism_count = int(self.elitism_rate * self.population_size)
        selected_elites = self.population[:self.population_size - elitism_count]
        selected_parents = self._roulette_wheel_selection(self.population_size - elitism_count)
        selected_parents.extend(selected_elites)
        return selected_parents
    
    def _roulette_wheel_selection(self, k) -> list[PermSolution]:
        """Performs roulette wheel selection on the population. Returns a list of selected parents."""
        total_fitness = sum(self._fitness(individual) for individual in self.population)
        probabilities = [1 - (self._fitness(individual) / total_fitness) for individual in self.population]
        return random.choices(self.population, weights=probabilities, k=k)
    
    def _crossover(self, parents):
        """Performs crossover on selected parents. If crossover fails more than crossover_max_attempts then the parent is added to the children."""
        children = []
        for i in range(0, len(parents) - 1, 2):
            cross_func = self.crossover_function if self.crossover_function is not None else random.choice([halve_and_swap, extract_and_random_pick, choice_from_one_order_from_other])
            for parent_a, parent_b in [(parents[i], parents[i+1]), (parents[i+1], parents[i])]:
                for _ in range(self.crossover_max_attempts):
                    child = cross_func(parent_a, parent_b, self.packs, self.max_volume, self.max_weight, self.max_distance, self.min_chosen_packs, self.start_address)
                    if self._verify(child):
                        children.append(child)
                        break
                else:
                    # print('Crossover failed.')
                    children.append(parent_a)
        return children
    
    def _mutate(self, children):
        """Performs mutation on selected children. If mutation fails more than mutation_max_attempts then the child is not mutated."""
        for i in range(len(children)):
            if random.random() < self.mutation_rate:
                mutate_func = self.mutation_function if self.mutation_function is not None else random.choice([inverse_permutation, shift_block, shuffle_block, inverse_packages, cut_out_packs, add_packs])
                for _ in range(self.mutation_max_attempts):
                    child_copy = PermSolution(children[i].choice.copy(), children[i].perm.copy())
                    mutate_func(child_copy)
                    if self._verify(child_copy):
                        children[i] = child_copy
                        break
                else:
                    # print('Mutation failed.')
                    pass

    def _replace(self, crossed_children):
        """Replaces the population with the children."""
        self.population = sorted(crossed_children, key=self._fitness)
        if self._fitness(self.population[0]) < self.best_score:
            self.best_score = self._fitness(self.population[0])
            self.best_individual = self.population[0]
        self.scores.append(self.best_score)

    def display(self):
        """Displays the graph of the best score in each generation."""
        x = [i for i in range(self.max_generations)]
        plt.plot(x, self.scores)
        plt.show()



if __name__ == '__main__':

    max_volume = 30
    max_weight = 30
    max_distance = 200
    min_chosen_packs = 5
    start_address = (0, 0)
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


    ga = GeneticAlgorithm(max_volume, max_weight, max_distance, min_chosen_packs, start_address, packs, 
                          population_size=1500, 
                          max_generations=300, 
                          mutation_rate=0.2,
                          elitism_rate=0.25, 
                          crossover_max_attempts=10,
                          mutation_max_attempts=10,
                          alpha=1.25
                          )
    ga.run()
    print(f"Last Population's best individual:\n{ga.best_individual}")
    # ga.display()