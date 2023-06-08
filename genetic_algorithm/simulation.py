import random
import time
from itertools import permutations

import matplotlib.pyplot as plt
import networkx as nx
from bitarray import bitarray
from cross import (
    choice_from_one_order_from_other,
    extract_and_random_pick,
    halve_and_swap,
    CROSS_DICT,
)
from generator import generate_initial_solutions
from matplotlib.figure import Figure
from mutation import (
    add_packs,
    cut_out_packs,
    inverse_packages,
    inverse_permutation,
    shift_block,
    shuffle_block,
    MUTATION_DICT,
)
from data_classes import (
    PermSolution,
    MatSolution,
    Point,
    Package,
    convert_to_package_list,
)


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

    def __init__(
        self,
        max_volume,
        max_weight,
        max_distance,
        min_chosen_packs,
        start_address,
        packs,
        population_size=100,
        max_generations=1000,
        max_iter_no_improvement=30,
        alpha=1.15,
        crossover_rate=0.1,
        mutation_rate=0.005,
        crossover_function=None,
        mutation_function=None,
        elitism_rate=0.1,
        crossover_max_attempts=1000,
        mutation_max_attempts=1000,
        log_every=1,
        output_file=None,
    ):
        self.population = []
        self.max_volume = max_volume
        self.max_weight = max_weight
        self.max_distance = max_distance
        self.min_chosen_packs = min_chosen_packs
        self.start_address = start_address
        self.packs = packs
        # for simplicity population_size is even
        self.population_size = population_size + population_size % 2
        self.max_generations = max_generations
        self.max_iter_no_improvement = max_iter_no_improvement
        self.alpha = alpha
        self.crossover_rate = crossover_rate
        self.crossover_function = crossover_function
        self.mutation_function = mutation_function
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        self.crossover_max_attempts = crossover_max_attempts
        self.mutation_max_attempts = mutation_max_attempts
        self.log_every = log_every
        self.best_score = float("inf")
        self.best_individual = None
        self.scores = []
        self.priority_packs_indexes = (pack[0] for pack in packs if pack[4] != 0)

        self.G = nx.DiGraph()
        self.packages_positions = [tuple(pckg[3]) for pckg in self.packs]
        self.G.add_node(self.start_address)
        self.G.add_nodes_from(self.packages_positions)
        self.pos = dict(
            zip(self.G.nodes, [tuple(start_address)] + self.packages_positions)
        )

        self.mutation_type_count = dict(
            zip(
                [
                    "add_packs",
                    "cut_out_packs",
                    "inverse_packages",
                    "inverse_permutation",
                    "shift_block",
                    "shuffle_block",
                ],
                [0 for _ in range(6)],
            )
        )
        self.cross_type_count = dict(
            zip(
                [
                    "choice_from_one_order_from_other",
                    "extract_and_random_pick",
                    "halve_and_swap",
                ],
                [0 for _ in range(3)],
            )
        )
        self.output_f = output_file

    def run(self):
        """Runs the genetic algorithm."""
        self._initialize_population()

        if self.output_f is not None:
            self.output_f.write(
                f"generation, best_score, generation_best_score, avg_population_age, new_solutions_count\n"
            )

        no_improvement_iter = 0
        for i in range(self.max_generations):
            if i % self.log_every == 0:
                average_population_age = self.average_population_age()
                new_solutions_count = self.new_solutions_count()
                print(
                    f"Generation {i: <{len(str(self.max_generations))}} | Best score: {self.best_score: < 16.10} | Current generation best score: {self._fitness(self.population[0]): < 16.10} | Avg population age: {average_population_age: < 16.10} | New solutions count: {new_solutions_count}"
                )
                if self.output_f is not None:
                    self.output_f.write(
                        f"{i: <{len(str(self.max_generations))}}, {self.best_score: < 16.10}, {self._fitness(self.population[0]): < 16.10}, {average_population_age: < 16.10}, {new_solutions_count}\n"
                    )
            # for individual in self.population:
            #     print(f"{individual.perm} | {self._fitness(individual)}")

            prev_best_score = self.best_score

            # Aging population - it seems that the solutions are stored by reference and there are multiple
            # references to the same solutions, that's why i use the was_aged flag
            for solution in self.population:
                if not solution.was_aged:
                    solution.age += 1
                    solution.was_aged = True
            for solution in self.population:
                solution.was_aged = False

            # Selection
            selected_parents = self._select()
            # Crossover
            crossed_children = self._crossover(selected_parents)
            # Mutation
            self._mutate(crossed_children)
            # Replacement
            self._replace(selected_parents, crossed_children)

            if self.best_score >= prev_best_score:
                no_improvement_iter += 1
            else:
                no_improvement_iter = 0

            if no_improvement_iter == self.max_iter_no_improvement:
                break

        # Printing the mutations and crossover stats
        print("Mutations:")
        for key, value in self.mutation_type_count.items():
            print(f"{key}: {value}")
        print("Crossovers:")
        for key, value in self.cross_type_count.items():
            print(f"{key}: {value}")

        # # Saving the stats into the output file
        # if self.output_f is not None:
        #     self.output_f.write(f"Mutations:\n")
        #     for key, value in self.mutation_type_count.items():
        #         self.output_f.write(f"{key}: {value}\n")
        #     self.output_f.write(f"Crossovers:\n")
        #     for key, value in self.cross_type_count.items():
        #         self.output_f.write(f"{key}: {value}\n")

    def _initialize_population(self) -> None:
        """Generates initial population of size 'population_size.'"""
        print("Initializing population...")
        self.population = sorted(
            generate_initial_solutions(
                self.max_volume,
                self.max_weight,
                self.max_distance,
                self.min_chosen_packs,
                self.start_address,
                self.packs,
                self.population_size,
            ),
            key=self._fitness,
        )
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
        if (
            sum(
                self.packs[individual.perm[i]][3].distance_to(
                    self.packs[individual.perm[i + 1]][3]
                )
                for i in range(len(individual.perm) - 1)
            )
            + self.start_address.distance_to(self.packs[individual.perm[0]][3])
            > self.max_distance
        ):
            return False
        return True

    def _fitness(self, individual: PermSolution) -> float:
        """Returns the fitness of the individual. The lower the better. Implemetation of objective function from presentation. For permutations of length 0 returns infinity."""
        score = float("inf")
        if len(individual.perm) != 0:
            total_weight = sum(self.packs[i][1] for i in individual.perm)
            score = total_weight * self.start_address.distance_to(
                self.packs[individual.perm[0]][3]
            )
            total_weight -= self.packs[individual.perm[0]][1]
            for i in range(1, len(individual.perm)):
                score += total_weight * self.packs[individual.perm[i - 1]][
                    3
                ].distance_to(self.packs[individual.perm[i]][3])
                total_weight -= self.packs[individual.perm[i]][1]

            k, n = len(individual.perm), len(self.packs)
            score /= (1 + k / n) ** self.alpha

        return score

    def _select(self):
        """Selects individuals for crossover. Mixed elitisim and roulette wheel selection. Returns a list of selected parents."""
        elitism_count = int(self.elitism_rate * self.population_size)
        selected_elites = self.population[: self.population_size - elitism_count]
        selected_parents = self._roulette_wheel_selection(
            self.population_size - elitism_count
        )
        selected_parents.extend(selected_elites)
        return selected_parents

    def _roulette_wheel_selection(self, k) -> list[PermSolution]:
        """Performs roulette wheel selection on the population. Returns a list of selected parents."""
        total_fitness = sum(self._fitness(individual) for individual in self.population)
        probabilities = [
            1 - (self._fitness(individual) / total_fitness)
            for individual in self.population
        ]
        return random.choices(self.population, weights=probabilities, k=k)

    def _crossover(self, parents):
        """Performs crossover on selected parents. If crossover fails more than crossover_max_attempts then the parent is added to the children."""
        children = []
        for i in range(0, len(parents) - 1, 2):
            if random.random() > self.crossover_rate:
                continue
            if (
                type(self.crossover_function) == list
                or type(self.crossover_function) == tuple
            ):
                cross_func = random.choice(self.crossover_function)
            else:
                cross_func = (
                    self.crossover_function
                    if self.crossover_function is not None
                    else random.choice(
                        [
                            halve_and_swap,
                            extract_and_random_pick,
                            choice_from_one_order_from_other,
                        ]
                    )
                )
            for parent_a, parent_b in [
                (parents[i], parents[i + 1]),
                (parents[i + 1], parents[i]),
            ]:
                for _ in range(self.crossover_max_attempts):
                    child = cross_func(
                        parent_a,
                        parent_b,
                        self.packs,
                        self.max_volume,
                        self.max_weight,
                        self.max_distance,
                        self.min_chosen_packs,
                        self.start_address,
                    )
                    if self._verify(child):
                        self.cross_type_count[cross_func.__name__] = (
                            self.cross_type_count[cross_func.__name__] + 1
                        )
                        children.append(child)
                        break
                else:
                    # print('Crossover failed.')
                    # children.append(parent_a)
                    pass
        return children

    def _mutate(self, children):
        """Performs mutation on selected children. If mutation fails more than mutation_max_attempts then the child is not mutated."""
        for i in range(len(children)):
            if random.random() < self.mutation_rate:
                if (
                    type(self.mutation_function) == list
                    or type(self.mutation_function) == tuple
                ):
                    mutate_func = random.choice(self.mutation_function)
                else:
                    mutate_func = (
                        self.mutation_function
                        if self.mutation_function is not None
                        else random.choice(
                            [
                                inverse_permutation,
                                shift_block,
                                shuffle_block,
                                inverse_packages,
                                cut_out_packs,
                                add_packs,
                            ]
                        )
                    )
                for _ in range(self.mutation_max_attempts):
                    child_copy = PermSolution(
                        children[i].choice.copy(), children[i].perm.copy()
                    )
                    mutate_func(child_copy)
                    if self._verify(child_copy):
                        self.mutation_type_count[mutate_func.__name__] = (
                            self.mutation_type_count[mutate_func.__name__] + 1
                        )
                        children[i] = child_copy
                        break
                else:
                    # print('Mutation failed.')
                    pass

    def _replace(self, parents, children):
        """Replaces the population with the new population consisting of top parents and children."""
        self.population = sorted(parents + children, key=self._fitness)[
            : len(self.population)
        ]
        if self._fitness(self.population[0]) < self.best_score:
            self.best_score = self._fitness(self.population[0])
            self.best_individual = self.population[0]
        self.scores.append(self.best_score)

    def average_population_age(self) -> float:
        sum_of_ages = 0
        for solution in self.population:
            sum_of_ages += solution.age
        return sum_of_ages / len(self.population)

    def new_solutions_count(self) -> int:
        count = 0
        for solution in self.population:
            if solution.age == 0:
                count += 1
        return count

    def display(self, display=True) -> Figure:
        """Displays the graph of the best score in each generation."""
        fig, ax = plt.subplots()
        ax.plot([i for i in range(len(self.scores))], self.scores)
        ax.set_xlabel("Generation")
        ax.set_ylabel("Best score")
        ax.set_title("Best score in each generation")
        if display:
            plt.show()
        return fig

    def display_solution(self, permutation: list[int], display=True) -> Figure:
        fig, ax = plt.subplots()

        n = len(permutation)
        edges = [
            (self.start_address, self.packages_positions[permutation[0]]),
            (self.packages_positions[permutation[-1]], self.start_address),
        ]
        visited_nodes = set([self.start_address])
        for i in range(n - 1):
            edges.append(
                (
                    self.packages_positions[permutation[i]],
                    self.packages_positions[permutation[i + 1]],
                )
            )
            visited_nodes.add(self.packages_positions[permutation[i]])
            visited_nodes.add(self.packages_positions[permutation[i + 1]])

        self.G.add_edges_from(edges)

        nx.draw_networkx_nodes(self.G, pos=self.pos, ax=ax, node_size=250)
        nx.draw_networkx_nodes(
            self.G,
            pos=self.pos,
            ax=ax,
            nodelist=visited_nodes,
            node_size=250,
            node_color="r",
        )
        nx.draw_networkx_nodes(
            self.G,
            pos=self.pos,
            ax=ax,
            nodelist=[self.start_address],
            node_color="g",
            node_size=250,
        )
        nx.draw_networkx_edges(self.G, pos=self.pos, ax=ax, width=2)

        labels = {
            node: (index if index >= 0 else "S")
            for index, node in enumerate(self.G.nodes, start=-1)
        }
        nx.draw_networkx_labels(
            self.G,
            pos=self.pos,
            labels=labels,
            font_color="black",
            font_size=10,
            font_weight="bold",
            ax=ax,
        )

        if display:
            plt.show()
        return fig

    def exact_solution(self):
        """Brute force solution. Returns the exact solution of the problem. Works in reasonable time for small amount of packs."""
        start = time.time()
        best_individual = None
        best_score = float("inf")
        for i in range(self.min_chosen_packs, len(self.packs) + 1):
            for perm in permutations(range(len(self.packs)), i):
                choice = bitarray(len(self.packs))
                choice.setall(0)
                for j in perm:
                    choice[j] = 1
                individual = PermSolution(choice, perm)
                if self._verify(individual):
                    score = self._fitness(individual)
                    if score < best_score:
                        best_score = score
                        best_individual = individual
        print(f"Real solution: {best_individual} | {best_score}")
        end = time.time()
        print(f"Calculation time: {end - start}")

    def solution_stats(self, solution: PermSolution):
        """Returns statisitcs describint weight, volume, distance and amount of chosen packs in given solution and problem."""
        if len(solution.perm) != 0:
            total_weight = sum(self.packs[i][1] for i in solution.perm)
            total_volume = sum(self.packs[i][2] for i in solution.perm)
            total_distance = 0
            for i in range(1, len(solution.perm)):
                total_distance += self.packs[solution.perm[i - 1]][3].distance_to(
                    self.packs[solution.perm[i]][3]
                )
            pack_count = len(solution.perm)
        return f"{total_weight=} {total_volume=} {total_distance=} {pack_count=}"


if __name__ == "__main__":
    max_volume = 100
    max_weight = 120
    max_distance = 180
    min_chosen_packs = 8
    start_address = Point(0, 0)

    packs = [
        (0, 2, 1, (5, 25), 0),
        (1, 4, 8, (5, 1), 0),
        (2, 2, 10, (9, 14), 0),
        (3, 2, 7, (14, 13), 0),
        (4, 2, 2, (23, 29), 0),
        (5, 2, 8, (23, 14), 0),
        (6, 8, 7, (21, 17), 1),
        (7, 4, 5, (28, 27), 0),
        (8, 1, 3, (2, 14), 0),
        (9, 3, 7, (20, 5), 0),
        (10, 4, 1, (7, 6), 0),
        (11, 5, 1, (16, 26), 0),
        (12, 8, 6, (17, 29), 0),
        (13, 1, 1, (25, 21), 1),
        (14, 5, 7, (29, 17), 0),
        (15, 3, 1, (7, 9), 0),
        (16, 5, 3, (23, 4), 0),
        (17, 3, 8, (9, 23), 0),
        (18, 8, 6, (28, 7), 0),
        (19, 8, 9, (7, 29), 0),
        (20, 8, 1, (9, 17), 0),
        (21, 3, 1, (2, 24), 0),
        (22, 7, 8, (25, 27), 0),
        (23, 8, 1, (5, 12), 0),
        (24, 1, 4, (13, 2), 0),
        (25, 6, 4, (6, 15), 1),
        (26, 4, 6, (16, 6), 0),
        (27, 4, 2, (28, 20), 0),
        (28, 2, 5, (15, 17), 0),
        (29, 5, 1, (16, 9), 0),
    ]
    packs = convert_to_package_list(packs)

    ga = GeneticAlgorithm(
        max_volume,
        max_weight,
        max_distance,
        min_chosen_packs,
        start_address,
        packs,
        population_size=1500,
        max_generations=200,
        mutation_rate=0.1,
        elitism_rate=0.10,
        crossover_max_attempts=10,
        mutation_max_attempts=10,
        alpha=150,
    )
    # Don't use it for number of packs greater than 10. For 10 packs it takes about 1 minute, but time complexity is factorial.
    # ga.exact_solution()
    ga.run()
    print(f"Last Population's best individual:\n{ga.best_individual}")
    ga.display_solution(ga.best_individual.perm)
    ga.display()
