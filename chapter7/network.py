from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce
from layer import Layer
from util import sigmoid, derivative_sigmoid


T = TypeVar('T') # ニューラルネットワークの解釈の出力型


class Network:
    def __init__(self, layer_structure: List[int], learning_rate: float,
        activation_function: Callable[[float], float] = sigmoid,
        derivative_activation_function: Callable[[float], float] = derivative_sigmoid):
        if len(layer_structure) < 3:
            raise ValueError("Error: Should be at least 3 layers(1 input, 1 hidden, 1 output)")

        self.layers: List[Layer] = []
        input_layer: Layer = Layer(None, layer_structure[0], learning_rate, activation_function,
            derivative_activation_function)
        self.layers.append(input_layer)

        for previous, num_neurons in enumerate(layer_structure[1::]):
            next_layer = Layer(self.layers[previous], num_neurons, learning_rate, activation_function,
                derivative_activation_function)
            self.layers.append(next_layer)

    def outputs(self, input: List[float]) -> List[float]:
        return reduce(lambda inputs, layer: layer.outputs(inputs), self.layers, input)

    # 出力と期待値の誤差に基づき各ニューロンの変化を明確にする
    def backpropagate(self, expected: List[float]) -> None:
        # 出力層ニューロンのデルタ計算
        last_layer: int = len(self.layers) - 1
        self.layers[last_layer].calculate_deltas_for_output_layer(expected)
        # 逆順で隠れ層のデルタを計算
        for l in range(last_layer - 1, 0, -1):
            self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l + 1])

    # backpropagate()は重みの更新は行わないので重みの計算後に更新する処理を行う
    def update_weights(self) -> None:
        for layer in self.layers[1:]: # 入力層をスキップ
            for neuron in layer.neurons:
                for w in range(len(neuron.weights)):
                    neuron.weights[w] = neuron.weights[w] + (neuron.learning_rate * \
                        (layer.previous_layer.output_cache[w]) * neuron.delta)

    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        for location, xs in enumerate(inputs):
            ys: List[float] = expecteds[location]
            outs: List[float] = self.outputs(xs)
            self.backpropagate(ys)
            self.update_weights()

    def validate(self, inputs: List[List[float]], expecteds: List[T], interpret_output: Callable[[List[float]], T]) -> Tuple[int, int, float]:
        correct: int = 0
        for input, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(input))
            if result == expected:
                correct += 1
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage