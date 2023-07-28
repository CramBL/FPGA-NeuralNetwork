"""Basic plotting functionality"""
import matplotlib.pyplot as plt

SIGMOID_SIZE_BITS = [2, 3, 4, 5, 6, 7, 8, 9, 10]
SIGMOID_ACCURACY = [8.5, 8.5, 11.6, 94.1, 94.5, 95.0, 95.1, 95.1, 95.1]


if __name__ == "__main__":
    # Data for plotting
    x = SIGMOID_SIZE_BITS
    y = SIGMOID_ACCURACY

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.set_title('Sigmoid size vs. Accuracy (1000 predictions)', fontsize=20)
    ax.grid()
    plt.plot(x, y, marker='o', linestyle='dashed')
    # Annotate the values at each step
    for i, val in enumerate(x):
        ax.annotate(f'{y[i]:.1f}%', (val, y[i]),
                    textcoords="offset points", xytext=(0, 5), ha='center')

    # Increase the font size of the axis labels
    ax.set_xlabel("Sigmoid size [bits]", fontsize=16)
    ax.set_ylabel("Accuracy [%]", fontsize=16)

    plt.axhline(y=88.7, color='r', linestyle='-')
    plt.text(3.2, 90, 'ReLU: 88.7%', ha='left', va='center')

    # Remove white space around the figure
    plt.tight_layout()

    plt.show()
    fig.savefig("plots/sig-size-acc.svg", format="svg")
