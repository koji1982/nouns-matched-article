# %%
import requests
from bs4 import BeautifulSoup

result = requests.get('https://news.yahoo.co.jp/topics/domestic?page=4')
source = BeautifulSoup(result.text, 'html.parser')
newslinks = source.find_all("a", class_="newsFeed_item_link")

secondPage = requests.get(newslinks[0].get('href'))
articlehtml = BeautifulSoup(secondPage.text, 'html.parser')
secondlinks = articlehtml.find_all("a")
targeturl = ''
for source in secondlinks:
    if "続きを読む" in source.getText():
        targeturl = source.get('href')
        print(targeturl)

# articlehtml = requests.get(newslinks[0])
# articlesource = BeautifulSoup(articlehtml.text, 'html.parser')
# print(articlesource)

# %%
