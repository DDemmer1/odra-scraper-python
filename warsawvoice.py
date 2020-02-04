#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from datetime import date
import article


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    item = soup.find_all('div', class_='artTitle')
    item2 = soup.find_all('div', class_='newsTitle')
    item3 = soup.find_all('div', class_='newsTitleS')

    links = []
    for item in item:
        if item.find('a'):
            links.append(item.find('a').get('href').strip())

    for item in item2:
        if item.find('a'):
            links.append(item.find('a').get('href').strip())

    for item in item3:
        if item.find('a'):
            links.append(item.find('a').get('href').strip())
    return links


def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    # HEADLINE
    headline = ''
    hl = soup.find('div', class_='artTitle')
    if hl is not None:
        headline = hl.string

    # TOPIC
    topic = ''
    # AUTHOR
    author = ''

    # TEXT_BODY
    text_body = ''
    tb = soup.find('div', class_='artFull')
    for div in tb.find_all('div'):
        div.clear()

    text_body = tb.get_text()

    # CREATION_DATE
    creation_date = ''
    d = soup.find('div', class_='artDate')
    if d is not None:
        creationDate = d.string

    return article.Article(headline, link, text_body, 'http://www.warsawvoice.pl', 'warsawvoice', author, topic, date.today(), creation_date)
