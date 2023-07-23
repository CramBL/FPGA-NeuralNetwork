import matplotlib.pyplot as plt
import numpy as np

SIGMOID_SIZE = [2, 3, 4, 5, 6, 7, 8, 9, 10]
SIGMOID_ACCURACY = [8.5, 8.5, 11.6, 94.1, 94.5, 95.0, 95.1, 95.1, 95.1]


if __name__ == "__main__":
    # Data for plotting
    x = SIGMOID_SIZE
    y = SIGMOID_ACCURACY

    

    fig, ax = plt.subplots(figsize=(12, 6.75))

    ax.set(xlabel='Sigmoid size', ylabel='Accuracy [%]',
        title='Sigmoid size vs. Accuracy (1000 predictions)')
    ax.grid()
    plt.plot(x, y, marker='o', linestyle='dashed')  
    # Annotate the values at each step
    for i in range(len(x)):
        ax.annotate(f'{y[i]:.1f}%', (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center')
    
    # Remove white space around the figure
    plt.tight_layout()

    plt.show()
    fig.savefig("plots/sig-size-acc.svg", format="svg")