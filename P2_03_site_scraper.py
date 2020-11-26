import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from word2number import w2n
import shutil
import os
import time

main_url = 'http://books.toscrape.com/index.html'

def getAndParseURL(url):
	sauce = requests.get(url)
	soup = BeautifulSoup(sauce.text, features='html.parser')
	return(soup)

def getBooksURLs(url):
	soup = getAndParseURL(url)
	return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.find_all("article", class_="product_pod")])

soup = getAndParseURL(main_url)

category_refs = []
for ul in soup.find_all('ul', class_="nav nav-list"):
	for li in ul.find_all('li'):
		a = li.find('a')
		hrefs = a.get('href')
		category_refs.append(hrefs)

category_urls = []

for ref in category_refs:
	category_urls.append("/".join(main_url.split("/")[:-1]) + "/" + ref)

def paginator(url):
	soup = getAndParseURL(url)
	if len(soup.find_all("ul", class_ = "pager")) >= 1:
		while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:

			new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")

			pages_urls.append(new_url)

			soup = getAndParseURL(new_url)

