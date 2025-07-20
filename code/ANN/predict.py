# ----------------------------------------------------------------------
# This file is meant to return the classification label of the feature_vector. To get a new feature vector
# use the file vectorize.py. TO run this file simply use the standard run button.
# ----------------------------------------------------------------------

from keras.models import load_model
import numpy as np


def classify():

    input = np.load('feature_vector.npy').reshape(1, -1)


    prop_model = load_model('ANN\\prop_model.h5')


    y_pred_prob = prop_model.predict(input)
    y_pred = (y_pred_prob > 0.5).astype(int)

    if(y_pred==1):
        print("Propaganda")
    else:
        print("Non-Propaganda")