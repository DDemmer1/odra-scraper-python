from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import date
import article


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    items = soup.find_all('div', class_='trenner')

    links = []
    for item in items:
        if item.find('a'):
            link = item.find('a').get('href').strip()
            if "download" not in link:
                links.append(link)  # strip damit
    return links


def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    # HEADLINE
    headline = soup.find('h1').string

    # TOPIC
    topic = ''
    if len(soup.find_all('div', class_='category')) > 0:
        topic = soup.find_all('div', class_='category')[0].find('span').get('span')

    # AUTHOR
    author = ''
    if len(soup.find_all('span', class_='author')) > 0:
        author = soup.find_all('span', class_='author')[0].get_text()

    # TEXT_BODY
    text_body = soup.find_all('article', 'fullarticle')[0].get_text()
    text_body = ' '.join(text_body.split())

    # CREATION_DATE
    creation_date = ''
    if soup.find('time'):
        creation_date = soup.find('time').get('datetime')

    return article.Article(headline, link, text_body, 'http://www.german-times.com', 'german-times', author, topic,
                           date.today(), creation_date)
