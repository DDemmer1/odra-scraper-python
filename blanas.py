#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from datetime import date
import feedparser
import article


def get_news_links(url):
    rss = requests.get(url).content
    doc = feedparser.parse(rss)
    link_data = []
    if "naszdziennik.pl/" in url:
        for entry in doc['entries']:
            link_data.append({ 'link': entry['link'] })

    elif "blaetter.de/" in url:
        for entry in doc['entries']:
            # smtliche Übersichtsseiten herausfiltern
            non_articles_url_contains = [ "/dossiers/", '/kurzgefasst', '/chronik-des-monats' ]
            link = entry['link']
            if not any(x in link for x in non_articles_url_contains):
                link_data.append({'link': link, 'creation_date': entry['published']})

    return link_data


# Extrahiert alle notwendigen informationen von einem einzigen Artikel
def scrape(link, _creation_date = ''):

    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    source_url = ''
    source_name = ''
    headline = ''
    topic = ''
    author = ''
    text_body = ''
    creation_date = ''
    if "naszdziennik.pl/" in link:
        source_url = "https://naszdziennik.pl/"
        source_name = "Nasz Dziennik"

        # HEADLINE
        headline = soup.find('h1').string

        # TOPIC
        if soup.find(id='nav').find('a', class_='current'):
            topic = soup.find(id='nav').find('a', class_='current').string

        # AUTHOR
        if soup.find(id='article-author'):
            author = soup.find(id='article-author').string

        # TEXT_BODY
        if soup.find(id='article-subtitle'):
            subtitle = soup.find(id='article-subtitle').get_text()
        else:
            subtitle = ''
        body = soup.find(id='article-content').get_text()
        text_body = subtitle + '\n' + body

        # CREATION_DATE
        if soup.find(id='article-date'):
            creation_date = soup.find(id='article-date').string
            creation_date = ' '.join(creation_date.split())

    elif "blaetter.de/" in link:
        source_url = "https://blaetter.de/"
        source_name = "Blätter für deutsche und internationale Politik"

        # HEADLINE
        headline = "" if soup.find('h1', class_='heading--article') is None else soup.find('h1', class_='heading--article').find('span').string

        # Author
        if soup.findAll('div', class_='articleinfo'):
            for a in soup.findAll('div', class_='articleinfo'):
                if 'author--article' not in a.attrs['class']:
                    for t in a.findAll('a'):
                        author += t.string + ' '
        topic = ""

        # TEXT_BODY
        text_body = soup.find('div', class_='field--type-text-with-summary').getText()

        # CREATION_DATE
        creation_date = _creation_date

    return article.Article(headline.strip(), link, text_body.strip(), source_url, source_name, author.strip(), topic, date.today(), creation_date)

