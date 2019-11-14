#!/usr/bin/python

import requests
import re
import os
from bs4 import BeautifulSoup

url = 'https://www.foxnews.com/politics'
fn = 'titles.txt'
path = os.path.join(os.getcwd(), fn)

def get_titles(soup):
    titles = soup.find_all(re.compile('h[1-9]+'), class_='title')
    for title in titles:
        title_soup = title.find('a')
        if not title_soup:
            continue
        yield title_soup.contents[0]

def main():
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print('request denied')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    with open(path, 'w') as f:
        f.write('\n'.join(list(get_titles(soup))))

if __name__ == '__main__':
    main()
