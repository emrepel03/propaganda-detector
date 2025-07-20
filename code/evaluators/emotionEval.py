# ----------------------------------------------------------------------
# This file is meant to run by taking in the file path to a text file via the evaluate method
# and will return a score from 0-1 to represent how much emotionally charged language is in the text
# with 0 being the least and 1 being the most
# ----------------------------------------------------------------------


from openai import OpenAI
import re
import os
from .abstractEvaluator import abstractEvaluator

# Unique api key must be placed here in order to communicate with gpt
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# This class implements the abstractEvaluator class
class EmotionEval(abstractEvaluator): 


    # This method makes the actual call to gpt-3.5-turbo. It contains its instruction and will also feeed it a text passage to work with.
    # Additionally this method writes gpt's output into the output.txt file for later usage
    def callChat(self, text):

        import os
        article_path = os.path.join("evaluators", "TestArticle.txt")
        article = open(article_path, "r", encoding='utf-8').read()

        if text is None:
            text = article

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ("The following texts you will recieve will be news articles that may or may not contain elements of propaganda within. "
                                                "For each text I would like you to extract and return exact sentences from the article that contain examples of "
                                                "emotionally charged language, please number each one. Emotionally charged language does not include examples of text that is only deciet "
                                                "or manipulation. If you do not find any such examples then say 'I found none'. Additionally please "
                                                "explain your reasoning for choosing each example.")},
                    {"role": "user", "content": text}], 
            stream=True, seed = 2, temperature = 0
        )
        with open("evaluators\\output.txt", "w", encoding='utf-8') as file:
            for chunk in response:
                
                if chunk.choices[0].delta.content is not None:
                    #print(chunk.choices[0].delta.content, end="")
                    file.write(chunk.choices[0].delta.content)

            file.write("\n")
            
    # This method counts the toal number of sentences within the text passage that was given to gpt
    def count_sentences(self, text):
        sentences = re.split(r'[.!?]', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        return len(sentences)

    # This method counts the examples provided by gpt by reading its output text from the output.txt file
    def count_examples(self):
        examples = 0
        with open("evaluators\\output.txt", 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip() == '':
                    examples += 1
        
        return examples
    
    # This method simply uses a file path to read the text conent within the file 
    def read_text_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content



    # This method takes in a filepath and will use it to call gpt and create a score from 0-1 to be returned
    def evaluate(self, file):

        text = self.read_text_file(file)

        self.callChat(text)
        totalSentences = self.count_sentences(text)
        exampleSentences = self.count_examples()
        return (exampleSentences/totalSentences)


