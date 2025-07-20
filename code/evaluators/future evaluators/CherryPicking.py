#pip install sentence-transformers
#pip install googlesearch-python beautifulsoup4 requests
#pip install search-engine-parser
#pip install beautifulsoup4
#pip install googlepip install google
## This is cherrypicking evaluator and is not used in ANN but could be added if we decided to continue with the project 

from openai import OpenAI
import math
from sentence_transformers import SentenceTransformer
#from googlesearch import search

import requests
from bs4 import BeautifulSoup
import re
import spacy


from bs4 import BeautifulSoup
import requests




# Unique api key must be placed here in order to communicate with gpt
api_key = ""
client = OpenAI(api_key=api_key)


class CherryPicking(): 
     
     def callChat(self, text):
        
        if text is None:
            article = open("evaluators\\TestArticle.txt","r").read()
            text = article

      
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ("The following texts you will receive will be tweet or news article."
                                                " I want you to summarize the main idea of this text within one sentence"
                                                "Try to capture as much of the main idea as possible, including importnat names or event is apllicable"
                                                " The text is as follows:")},
                    {"role": "user", "content": text}], 
            stream=True, seed = 2, temperature = 0
        )
        
        summary = ""
        for chunk in response:
            if 'choices' in chunk and 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                summary += chunk.choices[0].delta.content
        return summary 
     
   
     
     
     def urlToText(self, url):
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            textContent = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            # p is for paragraph sections
            # h... are for the different headings
            # li is for items / bullet points

            extractedText = '\n'.join([p.get_text() for p in textContent if p.get_text().strip()])
            return extractedText
        else:
            print("Issue with requesting URL content")
            return None
     
      
     def get_cherry_picking_score(self, text):
        summary = self.callChat(text)  #First we get the summary of our text from openAI API
        embedding_summary = self.get_embedding(summary) # we get the vector embedding fo that summary 
        #print(embedding_summary)
        results = self.get_google_search_titles(summary) # we do a google search and retreve the url of the top 10 search result 
        
        
        score = 0
        for result in results:
            a = self.urlToText(result) # we get the text of the document using the webscraping i copied the method from webScrape.py 
            sum = self.callChat(a) # we summarise the document in one sentce using OPENAI API
            embedding_title = self.get_embedding(sum) # we also get the embedding of this summary 
           
            score += (1 - self.cosine_similarity(embedding_summary,embedding_title)) # add it to the score, we do 1 - x becuase we want 1 to indicate propaganda to be consistent with other evluators
        return score/10 #divide by the number of titles to get average 
     
     

    

     def cosine_similarity(vector1, vector2):
        dot_prod = sum(a * b for a, b in zip(vector1, vector2))
        mag1 = math.sqrt(sum(a * a for a in vector1))
        mag2 = math.sqrt(sum(a * a for a in vector2))
        return dot_prod / (mag1 * mag2)
     
     def get_embedding(self, text):
        
        embedding = self.embedding_model.encode(text)
        return embedding

     
     def get_google_search_titles(self, query):
        payload = {'api_key': 'XXX', 'q': query , 'gl': 'us', 'num': '10'} #have to add API KEY
        resp = requests.get('https://api.serpdog.io/search', params=payload)

        data = resp.json()

        links = [] 
        for result in data["organic_results"]:
            links.append(result)
        return links 

     
     
     def clean_title(self, title):
        # Remove any unwanted characters or extra whitespace
        title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with a single space
        title = re.sub(r'[^\w\s]', '', title)  # Remove any non-alphanumeric characters except spaces
        title = title.strip()  # Remove leading and trailing whitespace
        #many have a site nmae in their result and I want to remove them, but I struggle a bit with finding a good way to remove all words effectively so rn I decided to ask chatgpt for a list of site names and remove them if they are in there
        #this is not perfect but my solution for now, THINK OF BETTER IMPLEMENTATION IF TIME
        potential_site_names = [
            ' - Wikipedia', ' - BBC', ' - ABC News', ' - CNN', ' | Wikipedia', ' | BBC', ' | ABC News', ' | CNN',
            ' - The New York Times', ' - Reuters', ' - CNBC', ' - CBS News', ' - NPR', ' - The Guardian',
            ' - Fox News', ' | The New York Times', ' | Reuters', ' | CNBC', ' | CBS News', ' | NPR', ' | The Guardian',
            ' | Fox News', ' - Los Angeles Times', ' - The Washington Post', ' - USA TODAY', ' - Associated Press',
            ' | Los Angeles Times', ' | The Washington Post', ' | USA TODAY', ' | Associated Press',
            ' - Al Jazeera', ' - Politico', ' - HuffPost', ' - Business Insider', ' - Forbes',
            ' | Al Jazeera', ' | Politico', ' | HuffPost', ' | Business Insider', ' | Forbes',
            ' - ESPN', ' - Sports Illustrated', ' - Bleacher Report', ' | ESPN', ' | Sports Illustrated', ' | Bleacher Report',
            ' - National Geographic', ' - Scientific American', ' - Nature', ' - NASA', ' - Space.com',
            ' | National Geographic', ' | Scientific American', ' | Nature', ' | NASA', ' | Space.com',
            ' - IMDb', ' - Rotten Tomatoes', ' | IMDb', ' | Rotten Tomatoes'
        ]
        for site_name in potential_site_names:
            title = title.replace(site_name, '')
        return title
     
     def read_text_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

     def evaluate(self, file_path):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        text = self.read_text_file(file_path)
      
        score = self.get_cherry_picking_score(text)
        return score
     