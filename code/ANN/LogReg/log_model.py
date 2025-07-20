# ----------------------------------------------------------------------
# This file is for the creation and training of a logitic regression model as well as providing
# us with its precision and recall.
# ----------------------------------------------------------------------

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score


X_train = np.load('DATASETS/X_train.npy')
X_test = np.load('DATASETS/X_test.npy')
X_validation = np.load('DATASETS/X_validation.npy')

y_train = np.load('DATASETS/y_train.npy')
y_test = np.load('DATASETS/y_test.npy')
y_validation = np.load('DATASETS/y_validation.npy')

model = LogisticRegression(solver="liblinear", random_state=0)

model.fit(X_train, y_train)

y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(precision)
print(recall)
