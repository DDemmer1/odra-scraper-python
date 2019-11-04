#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import date

app = Flask(__name__)


class Article:
    def __init__(self, headline, link, text_body, source, source_name, author, topic, crawl_date, creation_date):
        self.headline = headline
        self.link = link
        self.text_body = text_body
        self.source = source
        self.source_name = source_name
        self.author = author
        self.topic = topic
        self.crawl_date = crawl_date
        self.creation_date = creation_date

    def serialize(self):
        return {
            'headline': self.headline,
            'textBody': self.text_body,
            'source': self.source,
            'source_name': self.source_name,
            'author': self.author,
            'topic': self.topic,
            'link': self.link,
            'crawl_date': self.crawl_date,
            'creation_date': self.creation_date,
        }


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    item = soup.find_all('div', class_='news-header')

    links = []
    for item in item:
        links.append(item.find('a').get('href').strip())
    return links


def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    # remove all script tags
    [s.extract() for s in soup('script')]

    # HEADLINE
    headline = soup.find('h1', class_='page-heading').string

    # TOPIC
    topic = ''
    if len(soup.find_all('div', class_='breadcrumbs')) > 0:
        topic = soup.find_all('div', class_='breadcrumbs')[0].find_all('a')[1].get('title')

    # AUTHOR
    author = ''
    if len(soup.find_all('div', class_='article-author')) > 0:
        author = soup.find_all('div', class_='article-author')[0].find('a').get_text()

    # TEXT_BODY
    text_body = soup.find_all('div', 'article-container')[0].get_text()
    text_body = ' '.join(text_body.split())

    # CREATION_DATE
    creation_date = ''
    if soup.find('time'):
        creation_date = soup.find('time').get('datetime')

    return Article(headline, link, text_body, 'http://pikio.pl', 'pikio', author, topic, date.today(), creation_date)


@app.route('/')
def get_articles():
    links = get_news_links('http://pikio.pl')
    articles = []
    for link in links:
        articles.append(scrape(link))
    return jsonify([e.serialize() for e in articles])


if __name__ == '__main__':
    app.run()
