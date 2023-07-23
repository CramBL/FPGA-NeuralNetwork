Fork of ZyNet (Based on work done here https://github.com/vipinkmenon/neuralNetwork) intended to be more modular and contain VHDL ports of Neuron models .

## Adjust weights, activation function etc.
Use the `mnistZyNet.py` script

```shell
$ python mnistZyNet.py --help
```


## Example performance

| Sigmoid Size | 2   | 3   | 4    | 5    | 6    | 7   | 8    | 9    | 10   |
| ------------ | --- | --- | ---- | ---- | ---- | --- | ---- | ---- | ---- |
| Accuracy [%] | 8.5 | 8.5 | 11.6 | 94.1 | 94.5 | 95  | 95.1 | 95.1 | 95.1 |

![sigsize-vs-accuracy](plots/sig-size-acc.svg)