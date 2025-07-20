from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import spacy
import math

from evaluators.abstractEvaluator import abstractEvaluator



nlp = spacy.load('en_core_web_sm')

class PosSentiment(abstractEvaluator):

    

    def tokenize(self, file_path): # takes txt files and tokenizes the tweet, using some basic preporcessing techniques and spacy lemmatizes the text
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                contents = file.read()
                
            #make lowercase remove links and remove # (idk if they actually had any but just in case i guess) 
                contents = contents.lower()
                contents = re.sub(r'http\S+|www\S+|https\S+', '', contents, flags=re.MULTILINE)
                contents = re.sub(r'#\w+', '', contents)
        
                doc = nlp(contents)
                #Perfroms lemmatization 
                cleaned_words = [
                    token.lemma_ for token in doc 
                    if not token.is_stop and not token.is_punct and not token.like_num and token.is_alpha
                ]
            
                return cleaned_words

        except FileNotFoundError:
            print('File not found error')
            return None

    def positive_sentiment_score(self, tokens):
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sent = 0
        for token in tokens:
            score = sentiment_analyzer.polarity_scores(token)
            if score['compound'] > 0: 
                sent += score['compound']
    
        sent = sent / len(tokens)  
    
        return sent


    def evaluate(self, file_path):
        tokens = self.tokenize(file_path)
        score  = self.positive_sentiment_score(tokens)
        return score
    
    

