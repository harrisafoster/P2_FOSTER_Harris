# P2_FOSTER_Harris
Web Scraper de projet 2

Ce web scraper peut récupérer toutes les données d'une page, catégory, ou le site entier de http://books.toscrape.com/ 
Il récupère les données, notamment product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url, et puis il les sort sous format .csv.
Le script P2_03_site_scraper.py récupère aussi toutes les images sous format de .jpg. 

## Installation
### Pour les développeurs (windows 10):
#### Clonez la source localement:
```sh
$ git clone https://github.com/harrisafoster/P2_FOSTER_Harris
$ cd P2_Foster_Harris
```
#### Créer et activer un environnement virtuel avec:
```sh
$ python -m venv env
$ source ./env/Scripts/activate
```
#### Et installez les packages requis avec:
```sh
$ pip install -r requirements.txt
```

## Utilisation
### Puis vous pouvez exécuter l'un des trois scripts dans votre terminal avec:
```sh
$ python P2_01_page_scraper.py
$ python P2_02_categorie_scraper.py
$ python P2_03_site_scraper.py
```
####Attention: Le script va prendre une dizaine de minutes pour terminer la récupération des données. Veuillez ne pas arrêter le script avant que ce soit terminé !

Pour utiliser P2_01 ou P2_02 avec de differentes pages ou catégories, il suffit de changer le variable "main_url" dans le code python pour exécuter ces scripts avec les lives ou catégories désirées. 
Le script P2_03 va automatiquement chercher toutes les catégories, livres, et données de chaque livre, y compris l'image, pour tout le site. 
Toutes les images sont stockées par catégorie dans des dossier distincts dénommé "nom_de_catégorie_image_files" dans le dossier créé "category_files" où vous trouverez également tous les fichiers .csv avec les données cherchées. 

Pour faciliter la lecture de ces données. Je vous conseille d'ouvrir les fichiers .csv en encoding UTF-8 et en Anglais(U.S.A.). Cela laissera Excel lire les données de type 'float' en nombre décimale et pas en texte. 

## Built with
Python 3.8
