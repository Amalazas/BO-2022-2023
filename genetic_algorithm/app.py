import click
import os
from simulation import GeneticAlgorithm
from gui import GUI, CROSS_DICT, MUTATION_DICT
from data_classes import Point, Package
import matplotlib.pyplot as plt


@click.group()
def run():
    """Select GUI or CLI"""


@run.command(help="Run the Graphical User Interface")
def gui():
    """Run the GUI"""
    app = GUI()
    app.run()


@run.command(help="Run the Command Line Interface")
@click.option(
    "-v",
    "--volume",
    type=float,
    help="Maximum volume of the packages that can be chosen",
)
@click.option(
    "-w",
    "--weight",
    type=float,
    help="Maximum weight of the packages that can be chosen",
)
@click.option(
    "-d", "--distance", type=float, help="Maximum distance that can be travelled"
)
@click.option("-mp", "--min_packs", type=int, help="Minimum number of selected packs")
@click.option(
    "-x", "--address_x", type=float, help="X coordinate of the starting address"
)
@click.option(
    "-y", "--address_y", type=float, help="Y coordinate of the starting address"
)
@click.option(
    "-f", "--file", type=str, help="Path to the input file", required=True, prompt=True
)
@click.option(
    "-p", "--population", type=int, default=1500, help="Size of the population"
)
@click.option(
    "-g", "--generations", type=int, default=200, help="Maximum number of iterations"
)
@click.option(
    "-ni",
    "--no_improve",
    type=int,
    default=30,
    help="Maximum number of iterations without improvement",
)
@click.option(
    "-a", "--alpha", type=float, default=2.0, help="Parameter of the objective function"
)
@click.option("-cr", "--crossover_rate", default=0.1, type=float, help="Crossover rate")
@click.option("-mr", "--mutation_rate", default=0.01, type=float, help="Mutation rate")
@click.option(
    "-cf",
    "--crossover_function",
    type=click.Choice(list(CROSS_DICT.keys())),
    default=["random"],
    multiple=True,
    help="Crossover function",
)
@click.option(
    "-mf",
    "--mutation_function",
    type=click.Choice(list(MUTATION_DICT.keys())),
    default=["random"],
    multiple=True,
    help="Mutation function",
)
@click.option("-er", "--elitism_rate", type=float, default=0.1, help="Elitism rate")
@click.option(
    "-cma",
    "--crossover_max_attempts",
    type=int,
    default=10,
    help="Maximum number of attempts to perform crossover",
)
@click.option(
    "-mma",
    "--mutation_max_attempts",
    type=int,
    default=10,
    help="Maximum number of attempts to perform mutation",
)
@click.option(
    "-le", "--log_every", type=int, default=1, help="Log info every x generations"
)
@click.option(
    "-bf",
    "--brute_force",
    is_flag=True,
    default=False,
    show_default=True,
    help="Run brute force instead of genetic algorithm",
)
def cli(**kwargs):
    """Run the CLI"""
    if not os.path.exists(kwargs["file"]):
        print(f"File {kwargs['file']} does not exist")
        return
    with open(kwargs["file"], "r") as f:
        start_address = Point(*map(float, f.readline().split()))
        V, M, D, h = f.readline().split()
        V, M, D = map(float, (V, M, D))
        h = int(h)
        packs = []
        line = f.readline()
        while line:
            index, weight, volume, x, y, priority = line.split()
            packs.append(
                Package(
                    int(index),
                    float(weight),
                    float(volume),
                    (float(x), float(y)),
                    int(priority),
                )
            )
            line = f.readline()
    if kwargs.get("volume") is not None:
        V = float(kwargs["volume"])
    if kwargs.get("weight") is not None:
        M = float(kwargs["weight"])
    if kwargs.get("distance") is not None:
        D = float(kwargs["distance"])
    if kwargs.get("min_packs") is not None:
        h = int(kwargs["min_packs"])
    if kwargs.get("address_x") is not None and kwargs.get("address_y") is not None:
        start_address = Point(float(kwargs["address_x"]), float(kwargs["address_y"]))
    mutation_functions = kwargs["mutation_function"]
    if "random" in mutation_functions:
        mutation_function = None
    else:
        mutation_function = [MUTATION_DICT[mutation] for mutation in mutation_functions]
    crossover_functions = kwargs["crossover_function"]
    if "random" in crossover_functions:
        crossover_function = None
    else:
        crossover_function = [
            CROSS_DICT[crossover] for crossover in crossover_functions
        ]

    ga = GeneticAlgorithm(
        max_volume=V,
        max_weight=M,
        max_distance=D,
        min_chosen_packs=h,
        start_address=start_address,
        packs=packs,
        population_size=int(kwargs["population"]),
        max_generations=int(kwargs["generations"]),
        max_iter_no_improvement=int(kwargs["no_improve"]),
        alpha=float(kwargs["alpha"]),
        crossover_rate=float(kwargs["crossover_rate"]),
        mutation_rate=float(kwargs["mutation_rate"]),
        crossover_function=crossover_function,
        mutation_function=mutation_function,
        elitism_rate=float(kwargs["elitism_rate"]),
        crossover_max_attempts=int(kwargs["crossover_max_attempts"]),
        mutation_max_attempts=int(kwargs["mutation_max_attempts"]),
        log_every=int(kwargs["log_every"]),
    )

    if bool(kwargs["brute_force"]):
        ga.exact_solution()
    else:
        ga.run()
        print(f"Stats: {ga.solution_stats(ga.best_individual)}")
        print(ga.best_individual)
        fig1 = ga.display_solution(ga.best_individual.perm, display=False)
        fig2 = ga.display(display=False)
        plt.show()
        

if __name__ == "__main__":
    run()
