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

category = soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3]

rating = soup.find("p", class_ = re.compile("star-rating")).get("class")[1]
rating = rating.lower()
rating_number = str((w2n.word_to_num(rating))) + "/5"

upc = soup.find("td").text

product_page_url = main_url

scraped_data = pd.DataFrame({'title': name, 'product_description': description, 'price_excluding_tax': price_without_tax, 'price_including_tax': price_with_tax, 'number_available': nb_in_stock, "image_url": img_url, 'category': category, 'review_rating': rating_number, 'universal_ product_code (upc)': upc, 'product_page_url': product_page_url}, index=[0])

scraped_data.to_csv("single_page_scrape.csv", encoding="latin1")