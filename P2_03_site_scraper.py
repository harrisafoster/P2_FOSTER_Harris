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

if os.path.exists('category_files'):
	shutil.rmtree('category_files')
time.sleep(.0000000000000001)
os.mkdir('category_files')

if os.path.exists('image_files'):
	shutil.rmtree('image_files')
time.sleep(.0000000000000001)
os.mkdir('image_files')

for url in category_urls[1:]:
	pages_urls = [url]
	paginator(url)
	books_URLs = []
	for page in pages_urls:
		books_URLs.extend(getBooksURLs(page))

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

	for url in books_URLs:
		soup = getAndParseURL(url)

		names.append(soup.find("div", class_ = re.compile("product_main")).h1.text)

		paragraphs = soup.find_all('p')
		if len(paragraphs[3].text) > 10:
			descriptions.append(paragraphs[3].text)
		else:
			descriptions.append("No description available.")

		tds = soup.find_all('td')
		prices_without_tax.append(float((tds[2].text).split("£")[1]))
		prices_with_tax.append(float((tds[3].text).split("£")[1]))

		nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text))

		img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))

		category = soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3]
		cleaned_category = ''.join(filter(str.isalpha, category))
		categories.append(cleaned_category)

		rating = soup.find("p", class_ = re.compile("star-rating")).get("class")[1]
		rating = rating.lower()
		ratings.append(w2n.word_to_num(rating))

		upcs.append(soup.find("td").text)

		product_page_urls.append(url)

	scraped_data = pd.DataFrame({'title': names, 'product_description': descriptions, 'price_excluding_tax': prices_without_tax, 'price_including_tax': prices_with_tax, 'number_available': nb_in_stock, "image_url": img_urls, 'category': categories, 'review_rating': ratings, 'universal_ product_code (upc)': upcs, 'product_page_url': product_page_urls})

	scraped_data.index += 1

	scraped_data.to_csv(categories[0] + '.csv', encoding="latin1")

	source = categories[0] + '.csv'
	destination = "category_files"

	shutil.move(source, destination)
	
	for url in img_urls:
		r = requests.get(url, allow_redirects=True)
		back_cut = url.rsplit("/", 7)[0]
		final_cut = back_cut.replace("http://books.toscrape.com/catalogue/", "")
		with open(final_cut + '.jpg', 'wb') as file_handle:
			file_handle.write(r.content)
		
		shutil.move(final_cut + '.jpg', "image_files")