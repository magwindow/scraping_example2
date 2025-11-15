import os
import re
import time
import random
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup

visited = []
def get_links(bs):
    links = bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    return [link for link in links if link not in visited]

def scrape_article(path):
    visited.append(path)
    html = requests.get(f'http://en.wikipedia.org{path}', headers={'User-Agent': 'Mozilla/5.0'}).text
    time.sleep(5)
    bs = BeautifulSoup(html, 'html.parser')
    print(f'Scraping {bs.find("h1").get_text()} in process {os.getpid()}')
    links = get_links(bs)
    if len(links) > 0:
        scrape_article(links[random.randint(0, len(links)-1)].attrs['href'])


processes = [
    Process(target=scrape_article, args=('/wiki/Kevin_Bacon',)),
    Process(target=scrape_article, args=('/wiki/Monty_Python',)) 
]

if __name__ == '__main__':
    [p.start() for p in processes]