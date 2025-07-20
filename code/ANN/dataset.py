# ----------------------------------------------------------------------
# This file is meant to be run by executing the command: "python -m ANN.dataset" within the terminal. It's purpose is to process
# batches of the text data and convert them into feature vectors. This process works in batches and each time it is run the previously processed
# data will be loaded, expanded upon and saved again.
#
# The amount of files processed in the batch can be altered in the main method where the parameter batch_size determines how many files will be
# processed from each group. Thus it should be noted that the total number of processed files will be double that of the input batch size.
#
# WARNING: This file does not function as intended when using automatic run buttons such as those present in the top right corner of VSCode. In 
# order to run it properly consult the top of this comment
#
#
# Processing is done in the following order: Emotion Eval, Stereotypes, PosGen, Emotional Lan, Loaded Lan, Bandwagon Lan
# ----------------------------------------------------------------------

from pathlib import Path
import os
import numpy as np
import glob
from sklearn.model_selection import train_test_split

from evaluators.emotionEval import EmotionEval
from evaluators.stereotypes import Stereotypes
from evaluators.Positive_Generalities_and_stereotypes.pos_gen import PosGen
from evaluators.riskWords.riskWords import RiskWords

from evaluators.riskWords.constants import EMOTIONAL_LANGUAGE
from evaluators.riskWords.constants import LOADED_LANGUAGE
from evaluators.riskWords.constants import BANDWAGON_LANGUAGE

from evaluators.riskWords.riskWordsLists import emotional_language
from evaluators.riskWords.riskWordsLists import loaded_language
from evaluators.riskWords.riskWordsLists import bandwagon_language

# Here is where instances of all our evaluators are created
emotionEvaluator = EmotionEval()
stereotypeEvaluator = Stereotypes()
posgenEvaluator = PosGen()
riskWords = RiskWords()

# This method takes in a specific file path and list of evaluators and uses them
# to give the text a score for each evaluator and then compile those scores into a numpy
# vector to be returned.
def compile_evaluations(file_path, evaluators):
    print("begin compilation")
    results = []
    for evaluator in evaluators:
        result = evaluator.evaluate(file_path)
        results.append(result)

    print("all except risk")

    results.append(riskWords.evaluate(file_path, emotional_language, EMOTIONAL_LANGUAGE))
    results.append(riskWords.evaluate(file_path, loaded_language, LOADED_LANGUAGE))
    results.append(riskWords.evaluate(file_path, bandwagon_language, BANDWAGON_LANGUAGE))

    return np.array(results)

# This method takes in a folder, evaluators, label batch size and start index in order
# to attempt to begin processing data for a specific folder at the previosuly left off point. 
# If no data had been processed thus far it will start from the beginning.
def process_folder(folder_path, evaluators, label, batch_size, start_index=0):
    all_results = []
    labels = []
    folder_path = Path(folder_path)
    
    file_num = 0
    files_processed = 0
    for filepath in glob.glob(os.path.join(folder_path, '*.txt')):
        if files_processed >= batch_size:
            break
        if file_num >= start_index:
            results_vector = compile_evaluations(filepath, evaluators)
            all_results.append(results_vector)
            labels.append(label)
            files_processed += 1
        print(file_num)
        file_num += 1

    print(file_num)

    return all_results, labels, file_num

# This method is meant to load all the previosuly processed data so that newly processed data can be
# added to what was processed before.
def load_existing_data(data_file, labels_file):
    if os.path.exists(data_file) and os.path.exists(labels_file):
        X = np.load(data_file, allow_pickle=True)
        y = np.load(labels_file, allow_pickle=True)
        return list(X), list(y)
    return [], []

# This method saves the feature vectors and the label vectors for the processed data
def save_combined_data(X, y, data_file, labels_file):
    np.save(data_file, np.array(X))
    np.save(labels_file, np.array(y))

# This method 
def retrieve_data(batch_size):
    evaluators = [emotionEvaluator, stereotypeEvaluator, posgenEvaluator]

    print("retrieving data")

    fake_tweets_folder = 'DATA/Fake_tweets txt files'
    true_tweets_folder = 'DATA/True_tweets txt files'

    # Load the index of the last processed files
    fake_checkpoint_file = 'fake_checkpoint_new.txt'
    true_checkpoint_file = 'true_checkpoint_new.txt'

    fake_start_index = 0
    true_start_index = 0

    if os.path.exists(fake_checkpoint_file):
        with open(fake_checkpoint_file, 'r') as f:
            fake_start_index = int(f.read())
    if os.path.exists(true_checkpoint_file):
        with open(true_checkpoint_file, 'r') as f:
            true_start_index = int(f.read())

    # Load prior data
    fake_data_file = 'DATA/fake_results_new.npy'
    fake_labels_file = 'DATA/fake_labels_new.npy'
    true_data_file = 'DATA/true_results_new.npy'
    true_labels_file = 'DATA/true_labels_new.npy'

    fake_results, fake_labels = load_existing_data(fake_data_file, fake_labels_file)
    true_results, true_labels = load_existing_data(true_data_file, true_labels_file)

    # Process propaganda folder
    new_fake_results, new_fake_labels, fake_last_index = process_folder(fake_tweets_folder, evaluators, 1, batch_size, fake_start_index)
    # Process non propaganda
    new_true_results, new_true_labels, true_last_index = process_folder(true_tweets_folder, evaluators, 0, batch_size, true_start_index)

    # Merge newly processed data with old data
    fake_results.extend(new_fake_results)
    fake_labels.extend(new_fake_labels)
    true_results.extend(new_true_results)
    true_labels.extend(new_true_labels)

    # Save new index for future checkpoint
    with open(fake_checkpoint_file, 'w') as f:
        f.write(str(fake_last_index))
    with open(true_checkpoint_file, 'w') as f:
        f.write(str(true_last_index))

    # Save combined data
    save_combined_data(fake_results, fake_labels, fake_data_file, fake_labels_file)
    save_combined_data(true_results, true_labels, true_data_file, true_labels_file)

    all_results_array = np.array(fake_results + true_results)
    y = np.array(fake_labels + true_labels)

    return all_results_array, y

# This method retrives dataset combining both labels of processed data and then shuffling them to
# change the order or their presentation.
def get_data_shuffled(batch_size):
    X, y = retrieve_data(batch_size)
    data = list(zip(X, y))
    np.random.shuffle(data)
    X_shuffled, y_shuffled = zip(*data)
    return np.array(X_shuffled), np.array(y_shuffled)

# This method splits the shuffled data into training, validation and test sets
def get_data_sets(batch_size):
    X, y = get_data_shuffled(batch_size)
    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=5)

    return X_train, X_validation, X_test, y_train, y_validation, y_test

# This method saves the complete split datasets for training, valdiationa and testing and saves them as their own files
# for later usage.
def save_data(X_train, X_validation, X_test, y_train, y_validation, y_test, folder_path='DATASETS'):
    os.makedirs(folder_path, exist_ok=True)

    print(f"X_train dimensions: {X_train.shape}")
    print(f"X_validation dimensions: {X_validation.shape}")
    print(f"X_test dimensions: {X_test.shape}")

    np.save(os.path.join(folder_path, 'X_train.npy'), X_train)
    np.save(os.path.join(folder_path, 'X_validation.npy'), X_validation)
    np.save(os.path.join(folder_path, 'X_test.npy'), X_test)
    np.save(os.path.join(folder_path, 'y_train.npy'), y_train)
    np.save(os.path.join(folder_path, 'y_validation.npy'), y_validation)
    np.save(os.path.join(folder_path, 'y_test.npy'), y_test)
    print(f"Data saved to {folder_path}")

# This method just deletes the saved checkpoints for the data folders. Really only used if
# data processing must be done from the begining.
def reset_start_index():
    fake_checkpoint_file = 'fake_checkpoint_new.txt'
    true_checkpoint_file = 'true_checkpoint_new.txt'
    
    if os.path.exists(fake_checkpoint_file):
        os.remove(fake_checkpoint_file)
        print(f"{fake_checkpoint_file} deleted.")
    if os.path.exists(true_checkpoint_file):
        os.remove(true_checkpoint_file)
        print(f"{true_checkpoint_file} deleted.")

# Main method of the file. Change the batch_size in order to alter how
# may files are processed in the batch.
if __name__ == "__main__":
    batch_size = 50
    X_train, X_validation, X_test, y_train, y_validation, y_test = get_data_sets(batch_size)
    save_data(X_train, X_validation, X_test, y_train, y_validation, y_test)
