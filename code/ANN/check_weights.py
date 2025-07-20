# ----------------------------------------------------------------------
# This file simply checks the precision and recall of the modified artificial neural network classifier. To use 
# just run the file.
# ----------------------------------------------------------------------

import numpy as np
from keras.models import Sequential, load_model

X_train = np.load('DATASETS/X_train.npy')

model = load_model('ANN/prop_model.h5')

first_dense_weights = model.layers[0].get_weights()[0]

input_nodes_mean_weights = np.mean(first_dense_weights, axis=1)

print("Average weights for each input node to the first dense layer:")
for i, mean_weight in enumerate(input_nodes_mean_weights):
    print(f"Input node {i+1}: {mean_weight}")
