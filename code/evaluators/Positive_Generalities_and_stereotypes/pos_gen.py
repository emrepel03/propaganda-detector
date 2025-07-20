


# THIS BY ITSELF IS NOT A GOOD PROPAGANDA DETECTOR, all it does if find the amount of positve word such as great or anything
#vader considers to be positve above our threshold and than applies to ratio of psoitive generalities to total words and passes i through sigmoid
# the idea being to detetc dispaportionatly high positive generalites. 

# anyway you can run this by using the evaluate method, which needs an input of a txt file and returns a score of 0-1 for that txt file 0 meaning no postive generalites 1 alot. 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import spacy
import math

from evaluators.abstractEvaluator import abstractEvaluator



nlp = spacy.load('en_core_web_sm')

class PosGen(abstractEvaluator):

    def function(self, x):# tries to change the representation of the ratio a bit to a bit more significant, might want to change this into smth better
        return x * (2 - x)

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

    def detect_positive_generalities(self, tokens):
        positive_generalities = ["great", "fantastic", "amazing", "wonderful", "excellent", "awesome", "superb", "outstanding", "incredible",
        "best", "brilliant", "remarkable", "fabulous", "splendid", "marvelous", "phenomenal", "terrific", "perfect",
        "inspiring", "majestic", "glorious", "thrilling", "unbelievable", "miraculous", "unforgettable", "extraordinary",
        "stellar", "exceptional", "awe-inspiring", "mind-blowing", "astounding", "legendary", "godlike",] #asked gpt to create this list
        detected_generalities = []

        sentiment_analyzer = SentimentIntensityAnalyzer()
        for token in tokens:
            # Check if its positive generality (out of our given list )
            if token in positive_generalities:
                detected_generalities.append(token)
            
            else:
                #looks for other words with high sentiment rating to compliment our exisitng list
                score = sentiment_analyzer.polarity_scores(token)
                if score['compound'] > 0.6:  # experiemtn with changing this variable 
                    detected_generalities.append(token)
        
        return detected_generalities

    def calculate_propaganda_score(self, tokens, detected_generalities):
        total_words = len(tokens)
        total_positive_generalities = len(detected_generalities)
        if(total_words) > 0 :
            propaganda_score = total_positive_generalities / total_words
            
        else: 
            propaganda_score = 0
        return self.function(propaganda_score)

    def evaluate(self, file_path):
        tokens = self.tokenize(file_path)
        generalties = self.detect_positive_generalities(tokens)
        score = self.calculate_propaganda_score(tokens, generalties)
        return score

