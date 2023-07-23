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

    neuron_file = "Sigmoid" # default
    if neuron_type == "relu" or neuron_type == "relu-vhdl":
        neuron_file = "ReLu"

    weight_array = utils.genWeightArray("WeigntsAndBiases"+neuron_file+"New.txt")
    bias_array = utils.genBiasArray("WeigntsAndBiases"+neuron_file+"New.txt")
    model.compile(
        pretrained="Yes",
        weights=weight_array,
        biases=bias_array,
        dataWidth=data_width,
        weightIntSize=weight_int_size,
        inputIntSize=input_int_size,
        sigmoidSize=sigmoid_size,
    )

    if args.make_project is True:
        print("Creating vivado project files as MyZyNetProject")
        zynet.makeXilinxProject('MyZyNetProject','xc7z020clg484-1')
        zynet.makeIP('MyZyNetProject')
        zynet.makeSystem('MyZyNetProject','myBlock2')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ZyNet')
    parser.add_argument("-n", "--neuron", type=str)
    parser.add_argument("-s", "--sigmoid-size", type=int)
    parser.add_argument("-m", "--make-project", action='store_true')


    args = parser.parse_args()


    print(f"Neuron type: {args.neuron}")

    if (
        args.neuron != "relu"
        and args.neuron != "sigmoid"
        and args.neuron != "relu-vhdl"
        and args.neuron != "sigmoid-vhdl"
    ):
        print("Neuron type must be relu, sigmoid, or relu-vhdl")
        exit(1)
    if args.neuron == "sigmoid-vhdl":
        print("Unfortunately Vivado lacks good support for VHDL I/O...")
        print("Maybe it has better support now? You can try to fix this if you know what you're doing")
        print("exiting...")
        exit(1)

    sigmoid_size = args.sigmoid_size
    if sigmoid_size is None:
        sigmoid_size = 5 # default
    if sigmoid_size > 10:
        print("WARNING - Sigmoid size larger than 10 might fail to synthesize")

    generate_mnist_zynet(
        data_width=16, # Default 16
        sigmoid_size=sigmoid_size,
        weight_int_size=4,
        input_int_size=1,
        neuron_type=args.neuron,
    )
