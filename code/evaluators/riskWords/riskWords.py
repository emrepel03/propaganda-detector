from dotenv import load_dotenv
import string
import os
import glob
from pathlib import Path

import re

load_dotenv()

from evaluators.riskWords.constants import *

from evaluators.riskWords.riskWordsLists import *


from evaluators.abstractEvaluator import abstractEvaluator


#import spacy

#nlp = spacy.load('en_core_web_sm')

class RiskWords(abstractEvaluator):

    def tokenize(self, file_path): # takes txt files and tokenizes the tweet, using some basic preporcessing techniques and spacy lemmatizes the text
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                contents = file.read()
                
            #make lowercase remove links and remove # (idk if they actually had any but just in case i guess) 
                contents = contents.lower()
                contents = re.sub(r'http\S+|www\S+|https\S+', '', contents, flags=re.MULTILINE)
                contents = re.sub(r'#\w+', '', contents)
        
                #doc = nlp(contents)
                #Perfroms lemmatization 
                # cleaned_words = [
                #     token.lemma_ for token in doc 
                #     if not token.is_stop and not token.is_punct and not token.like_num and token.is_alpha
                # ]
                cleaned_words = contents.split()
                return cleaned_words

        except FileNotFoundError:
            print('File not found error')
            return None


    def get_ratio_of_risk_words(self, file_path, amount_of_risk_words):
        try:
            with open(file_path, 'r',encoding="utf-8") as file:
                contents = file.read()
                words = contents.split()
                translation_table = str.maketrans('','', string.punctuation)
                return amount_of_risk_words/len([word.translate(translation_table).lower() for word in words])
        except FileNotFoundError:
            print('File not found error')
            return None
        


    def count_risk_words(self, cleaned_list, words):
        count = 0
        for word in cleaned_list:
            if word in words:
                count +=1
        return count      

    def process_folder(self, folder_path, risk_words):
        total_ratios = 0
        total_files = 0
        folder_path = Path(folder_path)
        print(folder_path)
        for filepath in glob.glob(os.path.join(folder_path, '*.txt')):
            total_files += 1
            ratio_of_risk_words = self.get_ratio_of_risk_words(filepath, self.count_risk_words(self.tokenize(filepath), risk_words))
            #print(total_files)
            total_ratios += ratio_of_risk_words

        print(total_ratios)
        print(total_files)
        print("Total ratio is: ", total_ratios/total_files)

    def evaluate(self, file_path, risk_words, type_of_risk_words):
        ratio = 0
        shifted1 = 0
        shifted2 = 0
        
        if type_of_risk_words == LOADED_LANGUAGE:
            ratio = self.get_ratio_of_risk_words(file_path, self.count_risk_words(self.tokenize(file_path), risk_words))
            shifted1 = ratio - RATIO_LOADED_TRUE
            if shifted1 <= 0:
                return 0
            if shifted1>= shifted2:
                return 1
            else:
                shifted2 = RATIO_LOADED_FAKE - RATIO_LOADED_TRUE
                return shifted1/shifted2
            
        if type_of_risk_words == EMOTIONAL_LANGUAGE:
            ratio = self.get_ratio_of_risk_words(file_path, self.count_risk_words(self.tokenize(file_path), risk_words))
            shifted1 = ratio - RATIO_EMOTIONAL_TRUE
            if shifted1 <= 0:
                return 0
            if shifted1>= shifted2:
                return 1
            else:
                shifted2 = RATIO_EMOTIONAL_FAKE - RATIO_EMOTIONAL_TRUE
                return shifted1/shifted2    

        if type_of_risk_words == BANDWAGON_LANGUAGE:
            ratio = self.get_ratio_of_risk_words(file_path, self.count_risk_words(self.tokenize(file_path), risk_words))
            shifted1 = ratio - RATIO_BANDWAGON_TRUE
            #print(shifted1)
            if shifted1 <= 0:
                return 0
            if shifted1>= shifted2:
                return 1
            else:
                shifted2 = RATIO_BANDWAGON_FAKE - RATIO_BANDWAGON_TRUE
                return shifted1/shifted2  
            



#Test evaluatiors
'''
riskwords = RiskWords()

folder_path = 'DATA\\Fake_tweets txt files'
total_ratios = 0
total_files = 0
folder_path = Path(folder_path)
print(folder_path)
for filepath in glob.glob(os.path.join(folder_path, '*.txt')):
    total_files += 1
    eval_score = riskwords.evaluate(filepath, emotional_language, EMOTIONAL_LANGUAGE)
    print(total_files)
    total_ratios += eval_score

print(total_ratios)
print(total_files)
print("Total score is: ", total_ratios/total_files)

'''
    ##print(tokenize('evaluators\\riskWords\\testFile.txt'))

    ##print(tokenize('evaluators\\riskWords\\testFile.txt'))


    #process_folder('DATA\True_tweets txt files', emotional_language )
    #amount_of_loaded_words =  count_risk_words(tokenize('evaluators\\riskWords\\testFile.txt'), riskWordsLists.loaded_language)
    #print('Amount of loaded words: ', amount_of_loaded_words)
    #print('This gives ratio: ', get_ratio_of_risk_words('evaluators\\riskWords\\testFile.txt', amount_of_loaded_words ))

    #print('Amount of emotional words: ', count_risk_words(tokenize('evaluators\\riskWords\\testFile.txt'), riskWordsLists.emotional_language))





