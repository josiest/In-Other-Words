#!/usr/bin/python

import requests
import re
import os
from bs4 import BeautifulSoup

url = 'https://www.foxnews.com/politics'
fn = 'titles.md'
path = os.path.join(os.getcwd(), fn)

def main():
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        with open(path, 'w') as f:
            f.write('# Request to Fox News headlines was denied!')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    titles = list(get_titles(soup))

    while True:
        run_system(titles)

def get_titles(soup):
    titles = soup.find_all(re.compile('h[1-9]+'), class_='title')
    for title in titles:
        title_soup = title.find('a')
        if not title_soup:
            continue
        yield title_soup.contents[0]

def run_system(titles):
    for i, title in enumerate(titles):
        word, replacement = get_response(title)
        titles[i] = title.replace(word, replacement)
        with open(path, 'w') as f:
            f.write('\n'.join('# {}'.format(line) for line in titles))

def get_response(title):
    prompt = 'What would you like to replace in:\n\n{}\n\n'.format(title)
    word = input(prompt)

    while not word or word not in title:
        word = input("Sorry, I couldn't find {} in the title:\n\n"+
                     "{}\n\n".format(title)+"What is something else you want "+
                     "to replace?\n\n")

    replacement = input("What would you like to replace "+
                        "{} with?\n\n".format(word))

    return word, replacement

if __name__ == '__main__':
    main()
