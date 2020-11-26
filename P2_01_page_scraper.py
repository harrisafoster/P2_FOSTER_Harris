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

tds = soup.find_all('td')
price_without_tax = tds[2].text
price_with_tax = tds[3].text

nb_in_stock = re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text)

img_url = main_url.replace("index.html", "") + soup.find("img").get("src")

