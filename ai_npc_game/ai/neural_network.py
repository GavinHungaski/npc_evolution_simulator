import numpy as np
import random

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize wiehgts and biases with random values
        self.weights_ih = np.random.randn(self.input_nodes, self.hidden_nodes) * 0.1
        self.weights_ho = np.random.randn(self.hidden_nodes, self.output_nodes) * 0.1
        self.bias_h = np.random.randn(1, self.hidden_nodes) * 0.1
        self.bias_o = np.random.randn(1, self.output_nodes) * 0.1

    def predict(self, inputs):
        # Converts inputs list to a NumPy array for matrix operations
        inputs = np.array(inputs).reshape(1, -1)

        # Calculate hidden layer outputs
        hidden_layer_output = np.dot(inputs, self.weights_ih) + self.bias_h
        hidden_layer_output = np.tanh(hidden_layer_output)

        # Calculate output layer outputs
        output = np.dot(hidden_layer_output, self.weights_ho) + self.bias_o
        output = np.tanh(output)

        return output.flatten()

    def crossover(self, other_network):
        child = NeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)

        # Crossover weights_ih
        split = random.randint(0, self.weights_ih.shape[0])
        child.weights_ih[:split, :] = self.weights_ih[:split, :]
        child.weights_ih[split:, :] = other_network.weights_ih[split:, :]

        # For biases, a simpler approach is to take them randomly from one parent
        child.bias_h = self.bias_h if random.random() > 0.5 else other_network.bias_h
        child.bias_o = self.bias_o if random.random() > 0.5 else other_network.bias_o

        return child

    def mutate(self, rate):
        # Mutate weights_ih
        for i in range(self.weights_ih.shape[0]):
            for j in range(self.weights_ih.shape[1]):
                if random.random() < rate:
                    self.weights_ih[i, j] += np.random.randn() * 0.1

        # Mutate weights_ho
        for i in range(self.weights_ho.shape[0]):
            for j in range(self.weights_ho.shape[1]):
                if random.random() < rate:
                    self.weights_ho[i, j] += np.random.randn() * 0.1
        
        # Mutate biases
        if random.random() < rate:
            self.bias_h += np.random.randn(1, self.hidden_nodes) * 0.1
        if random.random() < rate:
            self.bias_o += np.random.randn(1, self.output_nodes) * 0.1
