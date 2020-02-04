#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from datetime import date
import article


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    item = soup.find_all('div', class_='news_box_item')

    links = []
    for item in item:
        if item.find('a'):
            links.append(item.find('a').get('href').strip())
    return links



def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags
    # HEADLINE
    headline = soup.find('h1', class_='entry-title title post_title').string

    # TOPIC
    topic = soup.find('span', class_='article_dots cat').string

    # AUTHOR
    author = soup.find('div', class_='von').contents[2][1:]

    # TEXT_BODY
    text_body = soup.find('div', 'post_content_inner_wrapper content_inner_wrapper entry-content').get_text()

    # CREATION_DATE
    creation_date = soup.find('div', class_='von').find('span', class_='article_dots').string

    return article.Article(headline, link, text_body, 'https://www.theeuropean.de', 'theeuropean', author, topic, date.today(), creation_date)
