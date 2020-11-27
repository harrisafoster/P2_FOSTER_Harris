import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from word2number import w2n
import shutil
import os
import time
## URL du site à scraper
main_url = 'http://books.toscrape.com/index.html'
## Fonction pour faire une requête sur un URL, prendre et parser ses données HTML, puis les retourner en variable 'soup'
def getAndParseURL(url):
	sauce = requests.get(url)
	soup = BeautifulSoup(sauce.text, features='html.parser')
	return(soup)
## Fonction pour chercher les hrefs de chaque livre sur une page et ensuite les concaténer avec l'url de la page pour avoir un URL utilisable pour chaque page livre.
def getBooksURLs(url):
	soup = getAndParseURL(url)
	return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.find_all("article", class_="product_pod")])
## Définition du variable soup pour les blocs définissant la liste des URLs des catégories
soup = getAndParseURL(main_url)
## Défintion d'une liste pour stocker les hrefs des catégories, puis une boucle "for" pour les trouver et les stocker dans cette liste.
category_refs = []
for ul in soup.find_all('ul', class_="nav nav-list"):
	for li in ul.find_all('li'):
		a = li.find('a')
		hrefs = a.get('href')
		category_refs.append(hrefs)
## Création d'une liste pour stocker des URLs complètes de chaque URL de catégorie.
category_urls = []
## Boucle 'for' pour refaire des URLs complètes à partir de l'URL principal et les hrefs cherchés précédemment.
for ref in category_refs:
	category_urls.append("/".join(main_url.split("/")[:-1]) + "/" + ref)
## Défintion d'une fonction pour trouver et itérer toutes les pages d'une catégories si la catégorie contient plusieurs pages de livres.
def paginator(url):
	soup = getAndParseURL(url)
	if len(soup.find_all("ul", class_ = "pager")) >= 1:
		while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:

			new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")

			pages_urls.append(new_url)

			soup = getAndParseURL(new_url)
## Vérification de l'existence d'un dossier appelé 'category_files'. S'il existe, il est supprimé et ensuite recréé; Sinon, il est créé.
if os.path.exists('category_files'):
	shutil.rmtree('category_files')
time.sleep(.0000000000000001)
os.mkdir('category_files')
## Grande boucle 'for' qui fait toutes les actions inclues pour chaque catégorie de livres à l'exception de la première catégorie qui serait simplement "books". Donc ce n'est pas nécéssaire de télécharger des données pour 1000 livres deux fois.
for url in category_urls[1:]:
	## Création d'une liste 'pages_urls' pour stocker les URLs des pages trouvés par la paginator.
	pages_urls = [url]
	paginator(url)
	## Création d'une liste 'books_URLs' pour stocker les URLs des pages livres trouvés dans chaque page de chaque catégorie.
	books_URLs = []
	## Stockage de chaque page livre dans la liste 'books_URLS'
	for page in pages_urls:
		books_URLs.extend(getBooksURLs(page))
	## Création de toutes les listes nécéssaires pour stockers les données cherchées sur chaque page livre.
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
	## Création d'une boucle 'for' à l'intérieur de la boucle pour les catégories pour pouvoir chercher toutes ces information sur chaque livre dans chaque catégorie.
	for url in books_URLs:
		soup = getAndParseURL(url)
		## Recherche et ajout du titre(nom) à la liste concernée
		names.append(soup.find("div", class_ = re.compile("product_main")).h1.text)
		## Recherche, vérification, et ajout de la déscription à liste concerné si elle existe. 
		paragraphs = soup.find_all('p')
		if len(paragraphs[3].text) > 10:
			descriptions.append(paragraphs[3].text)
		else:
			descriptions.append("No description available.")
		## Recherche des deux cellules contenant l'information recherchée (prix hors taxe et le prix avec taxe), puis ajout aux listes concernées. 
		tds = soup.find_all('td')
		prices_without_tax.append(float((tds[2].text).split("£")[1]))
		prices_with_tax.append(float((tds[3].text).split("£")[1]))
		## Recherche et ajout du nombre disponible pui ajout à la liste concernée
		nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text))
		## Recherche du href de l'image, création d'un URL fonctionnel, puis ajout à la liste concernée.
		img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
		## Recherche du nom de la catégorie dans le href, édition de l'URL pour avoir un nom 'propre' puis ajout à la liste concernée
		category = soup.find("a", href = re.compile("../category/books/")).get("href").split("/")[3]
		cleaned_category = ''.join(filter(str.isalpha, category))
		categories.append(cleaned_category)
		## Recherche du "star-rating", conversion en classe 'int' puis ajout à la liste concernée
		rating = soup.find("p", class_ = re.compile("star-rating")).get("class")[1]
		rating = rating.lower()
		ratings.append(w2n.word_to_num(rating))
		## Recherce de la première cellule de la page, contenant l'UPC, conversion en texte, puis ajout à la liste concernée.
		upcs.append(soup.find("td").text)
		## Ajout simple de l'URL de la page livre à la liste concernée
		product_page_urls.append(url)
	## Création d'un tableau pandas avec les intitulés des colonnes et les instruction sur quelle liste il faut mettre dedans. 
	scraped_data = pd.DataFrame({'title': names, 'product_description': descriptions, 'price_excluding_tax': prices_without_tax, 'price_including_tax': prices_with_tax, 'number_available': nb_in_stock, "image_url": img_urls, 'category': categories, 'review_rating': ratings, 'universal_ product_code (upc)': upcs, 'product_page_url': product_page_urls})
	## Changement de l'index du tableau pour que la liste commence à '1' et pas à '0'.
	scraped_data.index += 1
	## Conversion et stockage des données dans un fichier .csv intitulé avec la catégorie actuelle. 
	scraped_data.to_csv(categories[0] + '.csv', encoding="latin1")
	## Définition des variables pour faciliter le déplacement des fichiers .csv produits. 
	source = categories[0] + '.csv'
	destination = "category_files"
	## Déplacement des fichiers .csv dans le dossier 'category_files'.
	shutil.move(source, destination)
	## Vérification/Création d'un sous-dossier de 'category_files' pour stocker les images appartenant à chaque catégorie
	if os.path.exists("category_files/" + categories[0] + "_image_files"):
		shutil.rmtree("category_files/" + categories[0] + "_image_files")
	time.sleep(.0000000000000001)
	os.mkdir("category_files/" + categories[0] + "_image_files")
	## Création d'une boucle 'for' pour chercher, télécharger, nommer et déplacer correctement tous les fichier images de la catégorie actuelle
	for url in img_urls:
		r = requests.get(url, allow_redirects=True)
		back_cut = url.rsplit("/", 7)[0]
		final_cut = back_cut.replace("http://books.toscrape.com/catalogue/", "")
		with open(final_cut + '.jpg', 'wb') as file_handle:
			file_handle.write(r.content)

		shutil.move(final_cut + '.jpg', "category_files/" + categories[0] + "_image_files")