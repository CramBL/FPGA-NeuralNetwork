""" Script for making changes to the neuron model in zynet. """
import argparse
from zynet import zynet
from zynet import utils


def generate_mnist_zynet(
    data_width: int,
    sigmoid_size: int,
    weight_int_size: int,
    input_int_size: int,
    neuron_type: str,
):
    """Generate a zynet model for mnist."""
    model = zynet.model()
    model.add(zynet.layer("flatten", 784))
    model.add(zynet.layer("Dense", 30, neuron_type))
    model.add(zynet.layer("Dense", 30, neuron_type))
    model.add(zynet.layer("Dense", 10, neuron_type))
    model.add(zynet.layer("Dense", 10, neuron_type))
    model.add(zynet.layer("Dense", 10, "hardmax"))
    weight_array = utils.genWeightArray("WeigntsAndBiasesReLuNew.txt")
    bias_array = utils.genBiasArray("WeigntsAndBiasesReLuNew.txt")
    model.compile(
        pretrained="Yes",
        weights=weight_array,
        biases=bias_array,
        dataWidth=data_width,
        weightIntSize=weight_int_size,
        inputIntSize=input_int_size,
        sigmoidSize=sigmoid_size,
    )
    # zynet.makeXilinxProject('myProject1','xc7z020clg484-1')
    # zynet.makeIP('myProject1')
    # zynet.makeSystem('myProject1','myBlock2')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--neuron", type=str)
    args = parser.parse_args()
    print(f"Neuron type: {args.neuron}")

    if (
        args.neuron != "relu"
        and args.neuron != "sigmoid"
        and args.neuron != "relu-vhdl"
    ):
        print("Neuron type must be relu, sigmoid, or relu-vhdl")
        exit(1)

    generate_mnist_zynet(
        data_width=16,
        sigmoid_size=5,
        weight_int_size=4,
        input_int_size=1,
        neuron_type=args.neuron,
    )
