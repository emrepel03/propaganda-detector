# ----------------------------------------------------------------------
# This file is for the creation and training of the artificial neural network. It is trained to be a binary
# classifier based on the feature vectors processed from our data. Used by running the file
# ----------------------------------------------------------------------

import numpy as np
from keras.layers import Dense
from keras.models import Sequential, load_model
from keras.optimizers import Adam

#test oliver 2


X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')

X_train_old = np.load('DATASETS/X_train_old.npy')
X_test_old = np.load('DATASETS/X_test_old.npy')
X_validation_old = np.load('DATASETS/X_validation_old.npy')

y_train_old = np.load('DATASETS/y_train_old.npy')
y_test_old = np.load('DATASETS/y_test_old.npy')
y_validation_old = np.load('DATASETS/y_validation_old.npy')

X_train_old = X_train_old[:1500]
X_test_old = X_test_old[:500]
X_validation_old = X_validation_old[:500]

y_train_old = y_train_old[:1500]
y_test_old = y_test_old[:500]
y_validation_old = y_validation_old[:500]


def create_model():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=6, name="HiddenLayer"))
    model.add(Dense(1, activation='sigmoid', name = "OutputLayer"))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model


model = create_model()

model.fit(X_train, y_train, epochs=5, batch_size=4, validation_data=(X_validation, y_validation))


model.save('ANN/prop_model.h5')

model = create_model()
model.fit(X_train_old, y_train_old, epochs=5, batch_size=4, validation_data=(X_validation_old, y_validation_old))
model.save('ANN/prop_model_old.h5')


#loss, accuracy = model.evaluate(X_test, y_test)
#print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
