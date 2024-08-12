# -*- coding: utf-8 -*-
"""2022B3A71382G_Neural_Network

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V3ahHYvdxdbUrMJlb324hddI_44wqHSN
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'digit-recognizer:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-competitions-data%2Fkaggle-v2%2F3004%2F861823%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240812%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240812T181626Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D2e35d34f301ddeb6c55834a786b1718f5d9655391d30759399dc79ce9b21bc876247c45a37c2dfffe8d13da410dcd3a067265059fed3d7373bb16b067db2c5f24c01c0c59a700501bc5587ee21664d850a226cbf5f5bece197f9a798f84ce4d9d908f18a3c91d576c6a2e4a5bee45ddbf4fbf79c9a891040b1316520ef600b4c14d61093ed3c820f76f35b5056e22323dced4c1a3cb265aef18f713d97afaafdfc5cdeff9d5e88fce712e7fd3bb928330ad771b39f3865d43f4419acba0d041600d4fd739dc58afbf154ac82b1350e6a590873045da914dd7954cafa573de807c66bd2db0bf62c8c350eed207127a3c0d3b952cef2a7014f93a8c317e78abf5d'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

class Linear:
    def __init__(self, input_dim, output_dim):
        """
        Initializes a fully connected (linear) layer.

        Parameters:
        input_dim (int): The number of input features.
        output_dim (int): The number of output features.
        """
        self.weights = np.random.randn(input_dim, output_dim) * 0.01
        self.biases = np.zeros((1, output_dim))

    def forward(self, x):
        """
        Performs the forward pass through the linear layer.

        Parameters:
        x (ndarray): Input data of shape (n_samples, input_dim).

        Returns:
        ndarray: The output of the linear layer of shape (n_samples, output_dim).
        """
        self.input = x
        return np.dot(x, self.weights) + self.biases

    def backward(self, dout):
        """
        Performs the backward pass through the linear layer.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output of this layer.

        Returns:
        ndarray: Gradient of the loss with respect to the input of this layer.
        """
        self.dweights = np.dot(self.input.T, dout)
        self.dbiases = np.sum(dout, axis=0, keepdims=True)
        return np.dot(dout, self.weights.T)

    def update_params(self, lr):
        """
        Updates the parameters of the layer using the calculated gradients.

        Parameters:
        lr (float): Learning rate for the update.
        """
        self.weights -= lr * self.dweights
        self.biases -= lr * self.dbiases

class ReLU:
    def forward(self, x):
        """
        Applies the ReLU activation function.

        Parameters:
        x (ndarray): Input data.

        Returns:
        ndarray: Output after applying ReLU, with the same shape as input.
        """
        self.input = x
        return np.maximum(0, x)

    def backward(self, dout):
        """
        Computes the gradient of the loss with respect to the input of the ReLU function.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output of this layer.

        Returns:
        ndarray: Gradient of the loss with respect to the input of this layer.
        """
        return dout * (self.input > 0)

class Sigmoid:
    def forward(self, x):
        """
        Applies the Sigmoid activation function.

        Parameters:
        x (ndarray): Input data.

        Returns:
        ndarray: Output after applying Sigmoid, with the same shape as input.
        """
        self.output = 1 / (1 + np.exp(-x))
        return self.output

    def backward(self, dout):
        """
        Computes the gradient of the loss with respect to the input of the Sigmoid function.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output of this layer.

        Returns:
        ndarray: Gradient of the loss with respect to the input of this layer.
        """
        return dout * self.output * (1 - self.output)

class Tanh:
    def forward(self, x):
        """
        Applies the Tanh activation function.

        Parameters:
        x (ndarray): Input data.

        Returns:
        ndarray: Output after applying Tanh, with the same shape as input.
        """
        self.output = np.tanh(x)
        return self.output

    def backward(self, dout):
        """
        Computes the gradient of the loss with respect to the input of the Tanh function.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output of this layer.

        Returns:
        ndarray: Gradient of the loss with respect to the input of this layer.
        """
        return dout * (1 - self.output ** 2)

class Softmax:
    def forward(self, x):
        """
        Applies the Softmax activation function.

        Parameters:
        x (ndarray): Input data.

        Returns:
        ndarray: Output after applying Softmax, with the same shape as input.
        """
        exp_vals = np.exp(x - np.max(x, axis=1, keepdims=True))
        self.output = exp_vals / np.sum(exp_vals, axis=1, keepdims=True)
        return self.output

    def backward(self, dout):
        """
        Computes the gradient of the loss with respect to the input of the Softmax function.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output of this layer.

        Returns:
        ndarray: Gradient of the loss with respect to the input of this layer.
        """
        return dout  # Gradient computation depends on the specific loss function used

class CrossEntropyLoss:

    def forward(self, y_pred, y_true):
        """
        Computes the cross-entropy loss.

        Parameters:
        y_pred (ndarray): Predicted probabilities (output from softmax).
        y_true (ndarray): True labels, one-hot encoded.

        Returns:
        float: The cross-entropy loss.
        """
        samples = len(y_true)
        y_pred_clipped = np.clip(y_pred, 1e-15, 1 - 1e-15)
        correct_confidences = y_pred_clipped[range(samples), y_true]
        return -np.log(correct_confidences)

    def backward(self, y_pred, y_true):
        """
        Computes the cross-entropy loss.

        Parameters:
        y_pred (ndarray): Predicted probabilities (output from softmax).
        y_true (ndarray): True labels, one-hot encoded.

        Returns:
        float: The cross-entropy loss.
        """
        samples = len(y_true)
        grad = y_pred.copy()
        grad[range(samples), y_true] -= 1
        grad = grad / samples
        return grad

class MSELoss:
    def forward(self, y_pred, y_true):
        """
        Computes the Mean Squared Error (MSE) loss.

        Parameters:
        y_pred (ndarray): Predicted values.
        y_true (ndarray): True values.

        Returns:
        float: The MSE loss.
        """
        self.loss = np.mean((y_pred - y_true) ** 2)
        return self.loss

    def backward(self, dout):
        """
        Computes the gradient of the MSE loss.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output (usually 1).

        Returns:
        ndarray: Gradient of the loss with respect to the input.
        """
        return dout * 2 * (y_pred - y_true) / y_true.size

class SGD:
    def __init__(self, learning_rate=0.01):
        """
        Initializes the Stochastic Gradient Descent (SGD) optimizer.

        Parameters:
        learning_rate (float): The learning rate for the optimizer.
        """
        self.lr = learning_rate

    def step(self, layers):
        """
        Updates the parameters of the model's layers using the computed gradients.

        Parameters:
        layers (list): A list of layers in the model.
        """
        for layer in layers:
            if hasattr(layer, 'update_params'):
                layer.update_params(self.lr)

class Model:
    def __init__(self):
        """
        Initializes the model, creating an empty list of layers.
        """
        self.layers = []

    def add_layer(self, layer):
        """
        Adds a layer to the model.

        Parameters:
        layer: The layer to add to the model.
        """
        self.layers.append(layer)

    def compile(self, loss, optimizer):
        """
        Compiles the model by setting the loss function and optimizer.

        Parameters:
        loss: The loss function to use.
        optimizer: The optimizer to use.
        """
        self.loss = loss
        self.optimizer = optimizer

    def forward(self, x):
        """
        Performs a forward pass through all layers of the model.

        Parameters:
        x (ndarray): Input data.

        Returns:
        ndarray: Output of the model.
        """
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, dout):
        """
        Performs a backward pass through all layers of the model.

        Parameters:
        dout (ndarray): Gradient of the loss with respect to the output of the model.
        """
        for layer in reversed(self.layers):
            dout = layer.backward(dout)

    def train(self, x_train, y_train, epochs, batch_size):
        """
        Trains the model on the training data.

        Parameters:
        x_train (ndarray): Training data.
        y_train (ndarray): Training labels.
        epochs (int): Number of epochs to train for.
        batch_size (int): Number of samples per batch.
        """
        for epoch in range(epochs):
            for i in range(0, len(x_train), batch_size):
                x_batch = x_train[i:i+batch_size]
                y_batch = y_train[i:i+batch_size]

                y_pred = self.forward(x_batch)

                loss = self.loss.forward(y_pred, y_batch)

                dout = self.loss.backward(y_pred, y_batch)
                self.backward(dout)

                self.optimizer.step(self.layers)

            print(f'Epoch {epoch+1}/{epochs}, Loss: {loss}')

    def predict(self, x):
        """
        Generates predictions for the input data.

        Parameters:
        x (ndarray): Input data.

        Returns:
        ndarray: Predicted values.
        """
        return self.forward(x)

    def evaluate(self, x_test, y_test):
        """
        Evaluates the model on the test data.

        Parameters:
        x_test (ndarray): Test data.
        y_test (ndarray): Test labels.

        Returns:
        tuple: A tuple containing the loss and accuracy on the test set.
        """
        y_pred = self.predict(x_test)
        loss = self.loss.forward(y_pred, y_test)
        accuracy = np.mean(np.argmax(y_pred, axis=0) == np.argmax(y_test, axis=0))
        return loss, accuracy

    def save(self, filepath):
        """
        Saves the model's weights and biases to a file.

        Parameters:
        filepath (str): The file path where the model should be saved.
        """
        np.savez(filepath, *[layer.weights for layer in self.layers if hasattr(layer, 'weights')],
                 *[layer.biases for layer in self.layers if hasattr(layer, 'biases')])

    def load(self, filepath):
        """
        Loads the model's weights and biases from a file.

        Parameters:
        filepath (str): The file path from where the model should be loaded.
        """
        data = np.load(filepath)
        idx = 0
        for layer in self.layers:
            if hasattr(layer, 'weights'):
                layer.weights = data['arr_%d' % idx]
                idx += 1
            if hasattr(layer, 'biases'):
                layer.biases = data['arr_%d' % idx]
                idx += 1

#mnist_train = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
#mnist_test = pd.read_csv('/kaggle/input/digit-recognizer/test.csv')
#x_train = mnist_train.drop('label', axis=1).copy()
#x_test = mnist_test.copy()
#y_train = mnist_train['label'].copy()

data = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
data = np.array(data)
m, n = data.shape
np.random.shuffle(data) # shuffle before splitting into dev and training sets

data_dev = data[40000:42000].T
y_test = data_dev[0]
x_test = data_dev[1:n].T
print (y_test.shape)
print (x_test.shape)

data_train = data[0:40000].T
y_train = data_train[0]
x_train = data_train[1:n].T

print (y_train.shape)
print (x_train.shape)



# Define a simple neural network using the framework
model = Model()
model.add_layer(Linear(784, 128))
model.add_layer(ReLU())
model.add_layer(Linear(128, 10))
model.add_layer(Softmax())

# Compile the model with loss and optimizer
loss = CrossEntropyLoss()
optimizer = SGD(learning_rate=0.01)
model.compile(loss, optimizer)

# Assume x_train, y_train, x_test, y_test are preprocessed and available
# Train the model
model.train(x_train, y_train, epochs=10, batch_size=128)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f'Test Loss: {test_loss}, Test Accuracy: {test_accuracy}')
y_pred = model.predict(x_test)
print(y_test)
print(y_pred)

print(y_pred.shape)