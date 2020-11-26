import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from word2number import w2n

main_url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'

def getAndParseURL(url):
	sauce = requests.get(url)
	soup = BeautifulSoup(sauce.text, features='html.parser')
	return(soup)

def getBooksURLs(url):
	soup = getAndParseURL(url)
	return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.find_all("article", class_="product_pod")])

