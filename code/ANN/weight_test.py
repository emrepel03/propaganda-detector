# ----------------------------------------------------------------------
# This file simply checks the precision and recall of the modified artificial neural network classifiers. 
# It iterates through all 6 networks and returns the precision, recall and differences in those from the 
# original network.
# ----------------------------------------------------------------------

from keras.models import load_model
import numpy as np
from sklearn.metrics import precision_score, recall_score


X_test = np.load('DATASETS/X_test.npy')
y_test = np.load('DATASETS/y_test.npy')

def get_standard(X_test):

    prop_model = load_model('ANN\\prop_model.h5')

    y_pred_prob = prop_model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)

    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    return precision, recall

def calculate_metrics(model_path, X_test):

    prop_model = load_model(model_path)
    
    if 'feat1' in model_path:
        X_test_modified = np.delete(X_test, 0, axis=1)
    elif 'feat2' in model_path:
        X_test_modified = np.delete(X_test, 1, axis=1)
    elif 'feat3' in model_path:
        X_test_modified = np.delete(X_test, 2, axis=1)
    elif 'feat4' in model_path:
        X_test_modified = np.delete(X_test, 3, axis=1)
    elif 'feat5' in model_path:
        X_test_modified = np.delete(X_test, 4, axis=1)
    elif 'feat6' in model_path:
        X_test_modified = np.delete(X_test, 5, axis=1)
    else:
        raise ValueError("Unknown model path")
    
    y_pred_prob = prop_model.predict(X_test_modified)
    y_pred = (y_pred_prob > 0.5).astype(int)
    
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    return precision, recall

# List of model paths
model_paths = ['ANN/prop_feat1.h5', 'ANN/prop_feat2.h5', 'ANN/prop_feat3.h5', 
               'ANN/prop_feat4.h5', 'ANN/prop_feat5.h5', 'ANN/prop_feat6.h5']

# Calculate metrics for each model and print results
for model_path in model_paths:
    precision_standard, recall_standard = get_standard(X_test)
    precision, recall = calculate_metrics(model_path, X_test)
    print(f"Model: {model_path}")
    print(f"Precision: {precision}")
    print(f"Precision difference: {precision-precision_standard}")
    print(f"Recall: {recall}")
    print(f"Recall difference: {recall-recall_standard}")
    print()



prop_model = load_model('ANN\\prop_model.h5')


y_pred_prob = prop_model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print(precision)
print(recall)