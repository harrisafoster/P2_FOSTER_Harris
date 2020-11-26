import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from word2number import w2n

main_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

sauce = requests.get(main_url)
soup = BeautifulSoup(sauce.text, features='html.parser')

name = soup.find("div", class_ = re.compile("product_main")).h1.text

paragraphs = soup.find_all('p')
if len(paragraphs[3].text) > 10:
	description = paragraphs[3].text
else: 
	description = "No description available."