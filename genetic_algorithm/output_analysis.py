import sys
import matplotlib.pyplot as plt
import pandas as pd

# py output_analysis.py "test_output test_input_7.txt 3000 1000 60 7.95 0.7 0.05 halve_and_swap random 0.4 20 20 .csv"

if __name__ == "__main__":

    # Loading the file
    file_path  = "./output/" + sys.argv[1]
    df = pd.read_csv(file_path)

    # Printing 4 sublots in 1 figure
    fig = plt.figure(1)
    fig.suptitle(f"{sys.argv[1][12:-4]}")
    
    plt.subplot(2,2,1, title="Best Score", xlabel="Generation Number", ylabel="Score")
    plt.plot(df["generation"], df["best_score"], "tab:green")
    
    plt.subplot(2,2,2, title="Generation Best Score", xlabel="Generation Number", ylabel="Score")
    plt.plot(df["generation"], df["generation_best_score"], "tab:purple")
    
    plt.subplot(2,2,3, title="Average Population Age", xlabel="Generation Number", ylabel="Age")
    plt.plot(df["generation"], df["avg_population_age"], "tab:orange")
    
    plt.subplot(2,2,4, title="New Children Count", xlabel="Generation Number", ylabel="Children Count")
    plt.plot(df["generation"], df["new_solutions_count"], "tab:red")
    
    # Saving of the plot
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f'{file_path[:-4]}.png', dpi=100)
    
    # plt.show()