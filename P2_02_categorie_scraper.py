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

booksURLs = []
for page in pages_urls:
	booksURLs.extend(getBooksURLs(page))

names = []
prices_with_tax = []
prices_without_tax = []
nb_in_stock = []
img_urls = []
categories = []
ratings = []
upcs = []
product_page_urls = []
descriptions = []

for url in booksURLs:
	soup = getAndParseURL(url)

	names.append(soup.find("div", class_ = re.compile("product_main")).h1.text)

	paragraphs = soup.find_all('p')

	if len(paragraphs[3].text) > 10:
		descriptions.append(paragraphs[3].text)
	else: 
		descriptions.append("No description available.")

	tds = soup.find_all('td')
	prices_without_tax.append(tds[2].text)
	prices_with_tax.append(tds[3].text)

	nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text)) 

	img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))

	categories.append(soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3])

	rating = soup.find("p", class_ = re.compile("star-rating")).get("class")[1]
	rating = rating.lower()
	ratings.append(str((w2n.word_to_num(rating))) + "/5")

	upcs.append(soup.find("td").text)

	product_page_urls.append(url)

scraped_data = pd.DataFrame({'title': names, 'product_description': descriptions, 'price_excluding_tax': prices_without_tax, 'price_including_tax': prices_with_tax, 'number_available': nb_in_stock, "image_url": img_urls, 'category': categories, 'review_rating': ratings, 'universal_ product_code (upc)': upcs, 'product_page_url': product_page_urls})

scraped_data.to_csv("category_scrape.csv", encoding="latin1")