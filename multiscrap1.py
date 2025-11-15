import os
import re
import time
import random
import requests
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup

def task_delegator(task_queue, urls_queue):
    visited = ['/wiki/Kevin_Bacon', '/wiki/Monty_Python']
    task_queue.put('/wiki/Kevin_Bacon')
    task_queue.put('/wiki/Monty_Python')

    while 1:
        if not urls_queue.empty():
            links = [link for link in urls_queue.get() if link not in visited]
            for link in links:
                task_queue.put(link)

def get_links(bs):
    links = bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    return [link.attrs['href'] for link in links]

def scrape_article(task_queue, urls_queue):
    while 1:
        while task_queue.empty():
            time.sleep(.1)
        path = task_queue.get()
        html = requests.get(f'http://en.wikipedia.org{path}', headers={'User-Agent': 'Mozilla/5.0'}).text
        time.sleep(1)
        bs = BeautifulSoup(html, 'html.parser')
        print(f'Scraping {bs.find("h1").get_text()} in process {os.getpid()}')
        links = get_links(bs)
        urls_queue.put(links)

task_queue = Queue()
urls_queue = Queue()

processes = [
    Process(target=task_delegator, args=(task_queue, urls_queue,)),
    Process(target=scrape_article, args=(task_queue, urls_queue,)),
    Process(target=scrape_article, args=(task_queue, urls_queue,))
]

if __name__ == '__main__':
    try:
        [p.start() for p in processes]
    except KeyboardInterrupt:
        [p.terminate() for p in processes]