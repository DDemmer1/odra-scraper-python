#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


class Article:
    def __init__(self, headline, link, text_body, source, source_name, author, topic, crawl_date):
        self.headline = headline
        self.link = link
        self.text_body = text_body
        self.source = source
        self.source_name = source_name
        self.author = author
        self.topic = topic
        self.crawl_date = crawl_date

    def serialize(self):
        return {
            'headline': self.headline,
            'link': self.link,
            'textBody': self.text_body
        }


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    item = soup.find_all("div", class_="news-header")

    links = []
    for item in item:
        links.append(item.find('a').get('href').strip())
    return links


def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')

    headline = soup.find("div", class_="page-heading")
    text_body = soup.find_all("div", class_="breadbrumbs")[0]
    return Article(headline, link)


@app.route('/')
def get_articles():
    links = get_news_links("http://pikio.pl")
    articles = []
    for link in links:
        articles.append(scrape(link))
    return jsonify([e.serialize() for e in articles])


if __name__ == '__main__':
    app.run()
