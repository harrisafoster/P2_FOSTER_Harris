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

pages_urls = [main_url]

soup = getAndParseURL(pages_urls[0])

if len(soup.find_all("ul", class_ = "pager")) >= 1:
	while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:

		new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")
		
		pages_urls.append(new_url)

		soup = getAndParseURL(new_url)

