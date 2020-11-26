# P2_FOSTER_Harris
Web Scraper de projet 2

Ce web scraper peut récupérer toutes les données d'une page, catégory, ou le site entier de http://books.toscrape.com/ 
Il récupère les données, notamment product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url, et puis il les sort sous format .csv.
Le script P2_03_site_scraper.py récupère aussi toutes les images sous format de .jpg. 

## Installation
### For developers
Clone the source locally:
```sh
$ git clone https://github.com/harrisafoster/P2_FOSTER_Harris
$ cd P2_Foster_Harris
```
```sh
Créer et activer un environnement virtuel avec:
$ python -m venv env
$ source ./env/Scripts/activate
$ pip install -r requirements.txt
```
Puis vous pouvez exécuter l'un des trois scripts avec:
```sh
$ python P2_01_page_scraper.py
$ python P2_02_categorie_scraper.py
$ python P2_03_site_scraper.py
```
## Utilisation
Pour utiliser P2_01 ou P2_02 avec de differentes pages ou catégories, il suffit de changer le variable "main_url" dans le code python pour exécuter ces scripts avec les lives ou catégories désirées. 
Le script P2_03 va automatiquement chercher toutes les catégories, livres, et données de chaque livre pour tout le site. 

## Built with
Python 3.8
