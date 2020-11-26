import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from word2number import w2n

main_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

sauce = requests.get(main_url)
soup = BeautifulSoup(sauce.text, features='html.parser')