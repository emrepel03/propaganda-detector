# ----------------------------------------------------------------------
# This file is for the creation and training of several artificial neural networks with slight modifications. Each
# one removes one of the features entirely, then trains and saves each one as a new network.
# ----------------------------------------------------------------------

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam


X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')


X_train_mod = X_train[:, 1:]
X_test_mod = X_test[:, 1:]
X_validation_mod = X_validation[:, 1:]



def create_model():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=5, name="HiddenLayer"))
    model.add(Dense(1, activation='sigmoid', name = "OutputLayer"))
    model.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model


for i in range(6):
    X_train_mod = np.delete(X_train, i, axis=1)
    X_test_mod = np.delete(X_test, i, axis=1)
    X_validation_mod = np.delete(X_validation, i, axis=1)

    model = create_model()

    model.fit(X_train_mod, y_train, epochs=5, batch_size=4, validation_data=(X_validation_mod, y_validation))
    model.save(f'ANN/prop_feat{i+1}.h5')