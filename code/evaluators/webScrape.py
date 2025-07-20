import requests

from bs4 import BeautifulSoup


#Takes in url in form of "___"
#Creates and saves a text file to the same directory as this. 
#https://en.wikipedia.org/wiki/Web_scraping -> Web_scraping.txt


def urlToTextFile(url):
    
    response = requests.get(url)

    #check if request was successful
    if response.status_code == 200:
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        textContent = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        #p is for paragraph sections
        #h... are for the different headings
        #li is for items / bullet points
        
        extractedText = '\n'.join([p.get_text() for p in textContent if p.get_text().strip()])
        outputTextFileName = url.split('/')[-1].split('.')[0] + '.txt'
        with open(outputTextFileName, 'w', encoding='utf-8') as file:
            file.write(extractedText)
    else:
        print("issue with requesting URL content")

urlToTextFile("https://en.wikipedia.org/wiki/Web_scraping")