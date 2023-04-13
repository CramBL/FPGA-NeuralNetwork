"""Generate the neural network files"""
import sys
import math
import os
from shutil import copyfile
from os import path

SOURCE_FILE_PATH = "./src/fpga/rtl/"
TB_FILE_PATH = "./src/fpga/tb/"


def write_include_file(
    pretrained, numDenseLayers, dataWidth, layers, sigmoidSize, weightIntSize
):
    # Create target Directory if don't exist
    if not os.path.exists(SOURCE_FILE_PATH):
        os.makedirs(SOURCE_FILE_PATH)
    if not os.path.exists(TB_FILE_PATH):
        os.makedirs(TB_FILE_PATH)
    f = open(SOURCE_FILE_PATH + "include.v", "w")
    if pretrained == "Yes":
        f.write("`define pretrained\n")
    f.write("`define numLayers " + str(numDenseLayers) + "\n")
    f.write("`define dataWidth " + str(dataWidth) + "\n")
    i = 1
    for i in range(1, len(layers)):
        f.write(f"`define numNeuronLayer{i} {layers[i].getNumNeurons()}\n")
        f.write(f"`define numWeightLayer{i} {layers[i - 1].getNumNeurons()}\n")
        f.write(f'`define Layer{i}ActType "{layers[i].getActivation()}"\n')
    f.write(f"`define sigmoidSize {sigmoidSize}\n")
    f.write(f"`define weightIntWidth {weightIntSize}\n")
    f.close()

    # resources_dir = path.join(path.dirname(__file__), "db/axi_lite_wrapper.v")
    copyfile(
        path.join(path.dirname(__file__), "db/axi_lite_wrapper.v"),
        SOURCE_FILE_PATH + "axi_lite_wrapper.v",
    )
    copyfile(
        path.join(path.dirname(__file__), "db/neuron.v"), SOURCE_FILE_PATH + "neuron.v"
    )
    copyfile(
        path.join(path.dirname(__file__), "db/relu.v"), SOURCE_FILE_PATH + "relu.v"
    )
    copyfile(
        path.join(path.dirname(__file__), "db/Sig_ROM.v"),
        SOURCE_FILE_PATH + "Sig_ROM.v",
    )
    copyfile(
        path.join(path.dirname(__file__), "db/Weight_Memory.v"),
        SOURCE_FILE_PATH + "Weight_Memory.v",
    )


def gen_layer(layerNum, numNeurons, actType):
    file_name = SOURCE_FILE_PATH + "Layer_" + str(layerNum) + ".v"
    with open(file_name, "w") as f:
        with open(path.join(path.dirname(__file__), "db/layerInterface")) as g:
            layer_data = g.read()
            f.write(
                f'module Layer_{layerNum} \
                    #(parameter NN = 30, \
                    # numWeight=784, \
                    # dataWidth=16, \
                    # layerNum=1, \
                    # sigmoidSize=10, \
                    # weightIntWidth=4, \
                    # actType="relu")\n'
            )
            f.write(layer_data)

            for i in range(numNeurons):
                f.write(
                    f'\nneuron #(.numWeight(numWeight),\
                    .layerNo(layerNum),\
                    .neuronNo({i}),\
                    .dataWidth(dataWidth),\
                    .sigmoidSize(sigmoidSize),\
                    .weightIntWidth(weightIntWidth),\
                    .actType(actType),\
                    .weightFile("w_{layerNum}_{i}.mif"),\
                    .biasFile("b_{layerNum}_{i}.mif"))\
                        n_{i}(\n\
                .clk(clk),\n\
                .rst(rst),\n\
                .myinput(x_in),\n\
                .weightValid(weightValid),\n\
                .biasValid(biasValid),\n\
                .weightValue(weightValue),\n\
                .biasValue(biasValue),\n\
                .config_layer_num(config_layer_num),\n\
                .config_neuron_num(config_neuron_num),\n\
                .myinputValid(x_valid),\n\
                .out(x_out[{i}*dataWidth+:dataWidth]),\n\
                .outvalid(o_valid[{i}])\n\
                );'
                )
            f.write("\nendmodule")


def gentb():
    copyfile(
        path.join(path.dirname(__file__), "db/top_sim.v"), TB_FILE_PATH + "top_sim.v"
    )


def gen_nn(
    numLayers=0,
    layers=[],
    dataWidth=0,
    pretrained="Yes",
    weights=[],
    biases=[],
    sigmoidSize=10,
    weightIntSize=1,
    inputIntSize=4,
):
    # Sanity checks
    if numLayers != len(layers):
        print(
            "Error: Number of specified layers does \
                not match with the layers provided"
        )
        sys.exit()

    if pretrained == "Yes":
        i = 0
        for layer in layers:
            if layer.type == "Dense" and layer.activation != "hardmax":
                try:
                    if layer.getNumNeurons() != len(weights[i]):
                        print(
                            f"Number of weights do not match with number of neurons for layer {i}"
                        )
                        sys.exit()
                    i += 1
                except Exception as exc:
                    raise RuntimeError(
                        "Number of weights do not match with number of neurons"
                    ) from exc
            elif layer.type == "Dense":
                i += 1
    else:
        i = 0
        for layer in layers:
            if layer.type == "Dense":
                i += 1

    write_include_file(
        pretrained, i, dataWidth, layers, sigmoidSize, weightIntSize
    )  # Write the include file

    with open(SOURCE_FILE_PATH + "zynet.v", "w") as f:
        with open(path.join(path.dirname(__file__), "db/moduleTemplate")) as g:
            data = g.read()
            f.write(data)

        f.write(
            """localparam IDLE = 'd0,
            SEND = 'd1;\n"""
        )
        # Instantiate the layers
        for i in range(1, numLayers):
            if layers[i].type == "Dense" and layers[i].activation != "hardmax":
                f.write(f"wire [`numNeuronLayer{i}-1:0] o{i}_valid;\n")
                f.write(
                    f"wire [`numNeuronLayer{i}\
                    *`dataWidth-1:0] x{i}_out;\n"
                )
                f.write(
                    f"reg [`numNeuronLayer{i}\
                    *`dataWidth-1:0] holdData_{i};\n"
                )
                f.write(f"reg [`dataWidth-1:0] out_data_{i};\n")
                f.write(f"reg data_out_valid_{i};\n\n")
                gen_layer(i, layers[i].getNumNeurons(), layers[i].getActivation)
                if i == 1:  # First layer input is connected to AXI
                    f.write(
                        f"Layer_{i} "
                        f"#(.NN(`numNeuronLayer{i}),"
                        f".numWeight(`numWeightLayer{i}),."
                        f"dataWidth(`dataWidth),.layerNum({i}),"
                        f".sigmoidSize(`sigmoidSize),"
                        f".weightIntWidth(`weightIntWidth),"
                        f".actType(`Layer{i}ActType)) "
                        f"l{i}(\n\t.clk(s_axi_aclk),\n\t.rst(reset),\n\t"
                        f".weightValid(weightValid),\n\t.biasValid(biasValid),"
                        f"\n\t.weightValue(weightValue),\n\t"
                        f".biasValue(biasValue),\n\t"
                        f".config_layer_num(config_layer_num),\n\t"
                        f".config_neuron_num(config_neuron_num),\n\t"
                        f".x_valid(axis_in_data_valid),\n\t"
                        f".x_in(axis_in_data),\n\t"
                        f".o_valid(o{i}_valid),\n\t"
                        f".x_out(x{i}_out)\n);\n\n"
                    )
                else:  # All other layers
                    f.write(
                        f"Layer_{i} \
                            #(.NN(`numNeuronLayer{i}),\
                            # .numWeight(`numWeightLayer{i}),\
                            # .dataWidth(`dataWidth),.layerNum({i}),\
                            # .sigmoidSize(`sigmoidSize),\
                            # .weightIntWidth(`weightIntWidth),\
                            # .actType(`Layer{i}ActType)) \
                            # l{i}(\n\t.clk(s_axi_aclk),\n\t\
                            # .rst(reset),\n\t\
                            # .weightValid(weightValid),\n\t\
                            # .biasValid(biasValid),\n\t\
                            # .weightValue(weightValue),\n\t.\
                            # biasValue(biasValue),\n\t\
                            # .config_layer_num(config_layer_num),\n\t\
                            # .config_neuron_num(config_neuron_num),\n\t\
                            # .x_valid(data_out_valid_{i - 1}),\n\t\
                            # .x_in(out_data_{i - 1}),\n\t\
                            # .o_valid(o{i}_valid),\n\t\
                            # .x_out(x{i}_out)\n);\n\n"
                    )

                if layers[i].activation != "hardmax":
                    f.write("//State machine for data pipelining\n\n")
                    f.write(f"reg       state_{i};\n")
                    f.write(f"integer   count_{i};\n")
                    f.write("always @(posedge s_axi_aclk)\n")
                    f.write(
                        f"begin\n\
        if(reset)\n\
        begin\n\
            state_{i} <= IDLE;\n\
            count_{i} <= 0;\n\
            data_out_valid_{i} <=0;\n\
        end\n\
        else\n\
        begin\n\
            case(state_{i})\n\
                IDLE: begin\n\
                    count_{i} <= 0;\n\
                    data_out_valid_{i} <=0;\n\
                    if (o{i}_valid[0] == 1'b1)\n\
                    begin\n\
                        holdData_{i} <= x{i}_out;\n\
                        state_{i} <= SEND;\n\
                    end\n\
                end\n\
                SEND: begin\n\
                    out_data_{i} <= holdData_{i}[`dataWidth-1:0];\n\
                    holdData_{i} <= holdData_{i}>>`dataWidth;\n\
                    count_{i} <= count_{i} +1;\n\
                    data_out_valid_{i} <= 1;\n\
                    if (count_{i} == `numNeuronLayer{i})\n\
                    begin\n\
                        state_{i} <= IDLE;\n\
                        data_out_valid_{i} <= 0;\n\
                    end\n\
                end\n\
            endcase\n\
        end\n\
    end\n\n"
                    )
            elif layers[i].activation == "hardmax":
                copyfile(
                    path.join(path.dirname(__file__), "db/maxFinder.v"),
                    SOURCE_FILE_PATH + "maxFinder.v",
                )
                f.write(
                    f"reg [`numNeuronLayer{i - 1}*\
                    `dataWidth-1:0] holdData_{i};\n"
                )
                f.write(
                    f"assign axi_rd_data = holdData_{i}\
                    [`dataWidth-1:0];\n\n"
                )
                f.write(
                    f"always @(posedge s_axi_aclk)\n\
        begin\n\
            if (o{i - 1}_valid[0] == 1'b1)\n\
                holdData_{i} <= x{i - 1}_out;\n\
            else if(axi_rd_en)\n\
            begin\n\
                holdData_{i} <= holdData_{i}>>`dataWidth;\n\
            end\n\
        end\n\n\n"
                )

                f.write(
                    f"maxFinder #(.numInput(`numNeuronLayer{i - 1}),\
                    .inputWidth(`dataWidth))\n\
        mFind(\n\
            .i_clk(s_axi_aclk),\n\
            .i_data(x{i - 1}_out),\n\
            .i_valid(o{i - 1}_valid),\n\
            .o_data(out),\n\
            .o_data_valid(out_valid)\n\
        );\n"
                )

        f.write("endmodule")

        f.close()

    gentb()

    with open(SOURCE_FILE_PATH + "sigContent.mif", "w") as f:
        fract_bits = sigmoidSize - (weightIntSize + inputIntSize)
        if (
            fract_bits < 0
        ):  # Sigmoid size is smaller the integer part of the MAC operation
            fract_bits = 0
        # Generating Sigmoid LUT content
        x = -(
            2 ** (weightIntSize + inputIntSize - 1)
        )  # Smallest input going to the Sigmoid LUT from the neuron
        for i in range(0, 2**sigmoidSize):
            y = sigmoid(x)
            z = DtoB(y, dataWidth, dataWidth - inputIntSize)
            f.write(z + "\n")
            x = x + (2**-fract_bits)

        f.close()


def DtoB(
    num, dataWidth, fracBits
):  # funtion for converting into two's complement format
    if num >= 0:
        num = num * (2**fracBits)
        num = int(num)
        e = bin(num)[2:]
    else:
        num = -num
        num = num * (2**fracBits)  # number of fractional bits
        num = int(num)
        if num == 0:
            d = 0
        else:
            d = 2**dataWidth - num
        e = bin(d)[2:]
    return e


def sigmoid(x):
    """Calculate sigmoid"""
    try:
        return 1 / (1 + math.exp(-x))
    except ValueError as exc:
        print(f"Error in sigmoid function: {exc}")
        return 0
