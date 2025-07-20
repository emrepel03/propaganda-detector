# ----------------------------------------------------------------------
# This file is meant to be run by executing the command: "python -m ANN.classify" within the terminal. This 
# file when run will ask to be provided with a text. Upon recieving it the text will be classified by the ann
# as propaganda or non-propaganda. To run this file on must put "python -m ANN.classify" into the terminal, then 
# enter the text you wish to classify when prompted.
# ----------------------------------------------------------------------

import numpy as np

from evaluators.emotionEval import EmotionEval

from evaluators.stereotypes import Stereotypes
from evaluators.Positive_Generalities_and_stereotypes.pos_gen import PosGen
from evaluators.riskWords.riskWords import RiskWords
from evaluators.riskWords.constants import EMOTIONAL_LANGUAGE, LOADED_LANGUAGE, BANDWAGON_LANGUAGE
from evaluators.riskWords.riskWordsLists import emotional_language, loaded_language, bandwagon_language

from keras.models import load_model



# Create instances of evaluators
emotionEvaluator = EmotionEval()
stereotypeEvaluator = Stereotypes()
posgenEvaluator = PosGen()
riskWords = RiskWords()

def compile_evaluations(file_path, evaluators):
    results = []
    for evaluator in evaluators:
        result = evaluator.evaluate(file_path)
        results.append(result)

    results.append(riskWords.evaluate(file_path, emotional_language, EMOTIONAL_LANGUAGE))
    results.append(riskWords.evaluate(file_path, loaded_language, LOADED_LANGUAGE))
    results.append(riskWords.evaluate(file_path, bandwagon_language, BANDWAGON_LANGUAGE))

    print(results)

    return np.array(results)


def classify():

    input = np.load('feature_vector.npy').reshape(1, -1)


    prop_model = load_model('ANN\\prop_model.h5')


    y_pred_prob = prop_model.predict(input)
    y_pred = (y_pred_prob > 0.5).astype(int)

    if(y_pred==1):
        print("Propaganda")
    else:
        print("Non-Propaganda")


def process_text(text, evaluators):
    temp_file_path = "temp_text.txt"
    with open(temp_file_path, "w") as file:
        file.write(text)

    feature_vector = compile_evaluations(temp_file_path, evaluators)

    print(feature_vector.shape)

    np.save("feature_vector.npy", feature_vector)
    


if __name__ == "__main__":

    text = input("Please enter the text to be evaluated: ")
    
    evaluators = [emotionEvaluator, stereotypeEvaluator, posgenEvaluator]
    
    process_text(text, evaluators)
    classify()
    #y_pred = predict(feature_vector)
    #print("Doc prediction", y_pred)
