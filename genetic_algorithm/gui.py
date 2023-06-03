import sys

import customtkinter as ctk
from cross import (
    choice_from_one_order_from_other,
    extract_and_random_pick,
    halve_and_swap,
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mutation import (
    add_packs,
    cut_out_packs,
    inverse_packages,
    inverse_permutation,
    shift_block,
    shuffle_block,
)
from simulation import GeneticAlgorithm

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


class GUI:
    """GUI for selecting parameters and showing results."""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Input")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", sys.exit)
        self.file_chosen = False

        # Variables
        self.max_volume_var = ctk.IntVar()
        self.max_weight_var = ctk.IntVar()
        self.max_distance_var = ctk.IntVar()
        self.min_chosen_packs_var = ctk.IntVar()
        self.start_address_x_var = ctk.IntVar()
        self.start_address_y_var = ctk.IntVar()
        self.population_size_var = ctk.IntVar()
        self.max_generations_var = ctk.IntVar()
        self.max_iter_no_improvement = ctk.IntVar()
        self.alpha_var = ctk.DoubleVar()
        self.mutation_rate_var = ctk.DoubleVar()
        self.elitism_rate_var = ctk.DoubleVar()
        self.crossover_max_attempts_var = ctk.IntVar()
        self.mutation_max_attempts_var = ctk.IntVar()
        self.log_every_var = ctk.IntVar()
        self.packs = []

        # Max Volume Input
        max_volume_label = ctk.CTkLabel(self.root, text="Max Volume")
        max_volume_label.grid(row=0, column=0, padx=5, pady=5)
        max_volume_entry = ctk.CTkEntry(self.root, textvariable=self.max_volume_var)
        max_volume_entry.grid(
            row=0, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Max Weight Input
        max_weight_label = ctk.CTkLabel(self.root, text="Max Weight")
        max_weight_label.grid(row=1, column=0, padx=5, pady=5)
        max_weight_entry = ctk.CTkEntry(self.root, textvariable=self.max_weight_var)
        max_weight_entry.grid(
            row=1, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Max Distance Input
        max_distance_label = ctk.CTkLabel(self.root, text="Max Distance")
        max_distance_label.grid(row=2, column=0, padx=5, pady=5)
        max_distance_entry = ctk.CTkEntry(self.root, textvariable=self.max_distance_var)
        max_distance_entry.grid(
            row=2, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Min Chosen Packs Input
        min_chosen_packs_label = ctk.CTkLabel(self.root, text="Min Chosen Packs")
        min_chosen_packs_label.grid(row=3, column=0, padx=5, pady=5)
        min_chosen_packs_entry = ctk.CTkEntry(
            self.root, textvariable=self.min_chosen_packs_var
        )
        min_chosen_packs_entry.grid(
            row=3, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Start Address Input
        start_address_label = ctk.CTkLabel(self.root, text="Start Address X Y")
        start_address_label.grid(row=4, column=0, padx=5, pady=5)
        start_address_x_entry = ctk.CTkEntry(
            self.root, textvariable=self.start_address_x_var
        )
        start_address_x_entry.grid(row=4, column=1, padx=5, pady=5)
        start_address_y_entry = ctk.CTkEntry(
            self.root, textvariable=self.start_address_y_var
        )
        start_address_y_entry.grid(row=4, column=2, padx=5, pady=5)

        # Population Size Input
        population_size_label = ctk.CTkLabel(self.root, text="Population Size")
        population_size_label.grid(row=5, column=0, padx=5, pady=5)
        population_size_entry = ctk.CTkEntry(
            self.root, textvariable=self.population_size_var
        )
        population_size_entry.grid(
            row=5, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Max Generations Input
        max_generations_label = ctk.CTkLabel(self.root, text="Max Generations")
        max_generations_label.grid(row=6, column=0, padx=5, pady=5)
        max_generations_entry = ctk.CTkEntry(
            self.root, textvariable=self.max_generations_var
        )
        max_generations_entry.grid(
            row=6, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Max Iter w/o Improvement Input
        max_iter_no_improvement = ctk.CTkLabel(
            self.root, text="Max Iter w/o Improvement"
        )
        max_iter_no_improvement.grid(row=7, column=0, padx=5, pady=5)
        max_iter_no_improvement = ctk.CTkEntry(
            self.root, textvariable=self.max_iter_no_improvement
        )
        max_iter_no_improvement.grid(
            row=7, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Alpha Input
        alpha_label = ctk.CTkLabel(self.root, text="Alpha")
        alpha_label.grid(row=8, column=0, padx=5, pady=5)
        alpha_entry = ctk.CTkEntry(self.root, textvariable=self.alpha_var)
        alpha_entry.grid(row=8, column=1, padx=5, pady=5, columnspan=2, sticky="nsew")

        # Mutation Rate Input
        mutation_rate_label = ctk.CTkLabel(self.root, text="Mutation Rate")
        mutation_rate_label.grid(row=9, column=0, padx=5, pady=5)
        mutation_rate_entry = ctk.CTkEntry(
            self.root, textvariable=self.mutation_rate_var
        )
        mutation_rate_entry.grid(
            row=9, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Elitism Rate Input
        elitism_rate_label = ctk.CTkLabel(self.root, text="Elitism Rate")
        elitism_rate_label.grid(row=10, column=0, padx=5, pady=5)
        elitism_rate_entry = ctk.CTkEntry(self.root, textvariable=self.elitism_rate_var)
        elitism_rate_entry.grid(
            row=10, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Crossover Max Attempts Input
        crossover_max_attempts_label = ctk.CTkLabel(
            self.root, text="Crossover Max Attempts"
        )
        crossover_max_attempts_label.grid(row=11, column=0, padx=5, pady=5)
        crossover_max_attempts_entry = ctk.CTkEntry(
            self.root, textvariable=self.crossover_max_attempts_var
        )
        crossover_max_attempts_entry.grid(
            row=11, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Mutation Max Attempts Input
        mutation_max_attempts_label = ctk.CTkLabel(
            self.root, text="Mutation Max Attempts"
        )
        mutation_max_attempts_label.grid(row=12, column=0, padx=5, pady=5)
        mutation_max_attempts_entry = ctk.CTkEntry(
            self.root, textvariable=self.mutation_max_attempts_var
        )
        mutation_max_attempts_entry.grid(
            row=12, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Log Every Input
        log_every_label = ctk.CTkLabel(self.root, text="Log Every")
        log_every_label.grid(row=13, column=0, padx=5, pady=5)
        log_every_entry = ctk.CTkEntry(self.root, textvariable=self.log_every_var)
        log_every_entry.grid(
            row=13, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Crossover Function dropdown
        crossover_function_label = ctk.CTkLabel(self.root, text="Crossover Function")
        crossover_function_label.grid(row=14, column=0, padx=5, pady=5)
        self.crossover_function_label_combo = ctk.CTkComboBox(
            self.root, values=list(CROSS_DICT.keys())
        )
        self.crossover_function_label_combo.grid(
            row=14, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Mutation Function dropdown
        mutation_function_label = ctk.CTkLabel(self.root, text="Mutation Function")
        mutation_function_label.grid(row=15, column=0, padx=5, pady=5)
        self.mutation_function_label_combo = ctk.CTkComboBox(
            self.root, values=list(MUTATION_DICT.keys())
        )
        self.mutation_function_label_combo.grid(
            row=15, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )

        # Packs File Input
        packs_file_label = ctk.CTkLabel(self.root, text="Packs File")
        packs_file_label.grid(row=16, column=0, padx=5, pady=5)
        packs_file_button = ctk.CTkButton(
            self.root, text="Select File", command=self._select_file
        )
        packs_file_button.grid(
            row=16, column=1, padx=5, pady=5, columnspan=2, sticky="nsew"
        )
        self.packs_text = ctk.CTkTextbox(self.root)
        self.packs_text.grid(
            row=17, column=0, padx=5, pady=5, sticky="nsew", columnspan=3
        )

        # Run Button
        self.run_button = ctk.CTkButton(
            self.root, text="Run", command=self._run_simulation
        )
        self.run_button.grid(
            row=18, column=0, padx=5, pady=5, columnspan=3, sticky="nsew"
        )

        # Default values
        self.max_volume_var.set(100)
        self.max_weight_var.set(120)
        self.max_distance_var.set(180)
        self.min_chosen_packs_var.set(8)
        self.start_address_x_var.set(0)
        self.start_address_y_var.set(0)
        self.population_size_var.set(1500)
        self.max_generations_var.set(200)
        self.max_iter_no_improvement.set(30)
        self.alpha_var.set(2)
        self.mutation_rate_var.set(0.01)
        self.elitism_rate_var.set(0.1)
        self.crossover_max_attempts_var.set(10)
        self.mutation_max_attempts_var.set(10)
        self.log_every_var.set(1)

        self.crossover_function_label_combo.set("random")
        self.mutation_function_label_combo.set("random")

    def run(self):
        """Runs the GUI."""
        self.root.mainloop()

    def _select_file(self):
        """Opens a file dialog and loads the file."""
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = ctk.filedialog.askopenfilename(
            title="Open a file", initialdir="/", filetypes=filetypes
        )
        self.file_chosen = True
        with open(filename, "r", encoding="utf-8") as f:
            x, y = map(int, f.readline().split())
            self.start_address_x_var.set(x)
            self.start_address_y_var.set(y)
            volume, weight, distance, min_chosen_packs = map(int, f.readline().split())
            self.max_volume_var.set(volume)
            self.max_weight_var.set(weight)
            self.max_distance_var.set(distance)
            self.min_chosen_packs_var.set(min_chosen_packs)
            self.packs_text.insert("1.0", f.read())

    def _run_simulation(self):
        """Runs the simulation and shows the results."""
        if self.file_chosen:
            self.run_button.configure(state="disabled")
            for i in self.packs_text.get("1.0", "end-1c").split("\n"):
                index, volume, weight, x, y, fragile = map(int, i.split())
                self.packs.append((index, volume, weight, (x, y), fragile))
            self.ga = GeneticAlgorithm(
                max_volume=self.max_volume_var.get(),
                max_weight=self.max_weight_var.get(),
                max_distance=self.max_distance_var.get(),
                min_chosen_packs=self.min_chosen_packs_var.get(),
                start_address=(
                    self.start_address_x_var.get(),
                    self.start_address_y_var.get(),
                ),
                packs=self.packs,
                population_size=self.population_size_var.get(),
                max_generations=self.max_generations_var.get(),
                max_iter_no_improvement=self.max_iter_no_improvement.get(),
                alpha=self.alpha_var.get(),
                mutation_rate=self.mutation_rate_var.get(),
                elitism_rate=self.elitism_rate_var.get(),
                crossover_max_attempts=self.crossover_max_attempts_var.get(),
                mutation_max_attempts=self.mutation_max_attempts_var.get(),
                log_every=self.log_every_var.get(),
                crossover_function=CROSS_DICT[
                    self.crossover_function_label_combo.get()
                ],
                mutation_function=MUTATION_DICT[
                    self.mutation_function_label_combo.get()
                ],
            )
            self.root.iconify()
            self.ga.run()

            self.results_frame = ctk.CTkFrame(self.root, width=600)
            self.results_frame.grid(
                row=0, column=4, padx=5, pady=5, sticky="nsew", columnspan=3, rowspan=18
            )
            print(self.ga.best_individual)
            print(f"Stats: {self.ga.solution_stats(self.ga.best_individual)}")
            fig1 = self.ga.display_solution(self.ga.best_individual.perm, display=False)
            fig2 = self.ga.display(display=False)
            canvas1 = FigureCanvasTkAgg(fig1, master=self.results_frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew", rowspan=1
            )
            canvas2 = FigureCanvasTkAgg(fig2, master=self.results_frame)
            canvas2.draw()
            canvas2.get_tk_widget().grid(
                row=1, column=0, padx=5, pady=5, sticky="nsew", rowspan=1
            )
            self.root.deiconify()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
