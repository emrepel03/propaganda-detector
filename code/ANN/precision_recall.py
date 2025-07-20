# ----------------------------------------------------------------------
# This file simply checks the precision and recall of the original artificial neural network classifier.
# It does this twice, once for the data collected with the old stereotype evaluator and once for the data
# collected with the new openai stereotype evaluator. To use just run the file.
# ----------------------------------------------------------------------

from keras.models import load_model
import numpy as np
from sklearn.metrics import precision_score, recall_score


X_test = np.load('DATASETS/X_test.npy')
y_test = np.load('DATASETS/y_test.npy')

X_test_old = np.load('DATASETS/X_test_old.npy')
y_test_old = np.load('DATASETS/y_test_old.npy')

X_test_old = X_test_old[:500]
y_test_old = y_test_old[:500]


prop_model_old = load_model('ANN\\prop_model_old.h5')


y_pred_prob = prop_model_old.predict(X_test_old)
y_pred = (y_pred_prob > 0.5).astype(int)

precision_old = precision_score(y_test_old, y_pred)
recall_old = recall_score(y_test_old, y_pred)

print(precision_old)
print(recall_old)




prop_model = load_model('ANN\\prop_model.h5')


y_pred_prob = prop_model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(precision)
print(recall)