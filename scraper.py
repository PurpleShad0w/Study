from bs4 import BeautifulSoup
import requests
from lxml import etree
import re
import pandas as pd


### The URL Scraper ###


next_page = ''
df = pd.DataFrame()
page_number = 5


for k in range(page_number):
    page = requests.get('https://theses.fr/fr/?q='+re.sub("'","",next_page))
    soup = BeautifulSoup(page.text, 'html.parser')
    dom = etree.HTML(str(soup))
    X_path_url = '//*[@id="resultat"]/div[1]/div[1]/h2/a'
    j = 1
    links = []
    for i in range(10):
        links.append('https://theses.fr'+dom.xpath(X_path_url)[0].get('href'))
        j = j+3
        X_path_url = '//*[@id="resultat"]/div['+str(j)+']/div[1]/h2/a'
    next_page_raw = dom.xpath('//*[@id="pagination"]/a[13]')[0].get('href')
    next_page = re.search('(\'(.*?)\')',next_page_raw).group(1)
    df = df.append(links)
    print('scraping page '+str(k+1)+'/'+str(page_number))

df.to_csv('url.csv')


### The Author Scraper ###


df2 = pd.DataFrame()

for k in range(len(df)):
    page = requests.get(df.iloc[k,0])
    soup = BeautifulSoup(page.text, 'html.parser')
    dom = etree.HTML(str(soup))
    authors = []
    try:
        authors.append(dom.xpath('//*[@id="ficheTitre"]/div[2]/h2/span')[0].text)
    except IndexError:
        authors.append(dom.xpath('//*[@id="ficheTitre"]/div[2]/h2/a/span')[0].text)
    df2 = df2.append(authors)
    print('scraping author '+str(k+1)+'/'+str(len(df)))

df2 = df2.drop_duplicates()
df2.to_csv('authors.csv')