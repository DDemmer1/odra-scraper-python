#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import date
import feedparser


# Article Klasse die die zu scrapenden Daten speichert
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

    # Helfer Methode die es später ermöglicht einen JSON String zu erstellen
    # siehe return von 'def get_articles()'
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


# Sucht sich die eine Liste mit allen Artikel links zusammen
def get_news_links(url):
    links = []
    data = feedparser.parse('http://www.tagesschau.de/xml/rss2')
    for item in data.entries:
        if 'livestream' not in item.link:
            links.append(item.link)
    return links


# Extrahiert alle notwendigen informationen von einem einzigen Artikel
def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    # CREATION_DATE
    creation_date = '' if soup.find('span', class_='stand') is None else soup.find('span', class_='stand').string

    # HEADLINE
    dachzeile = '' if soup.find('span', class_='dachzeile') is None else soup.find('span', class_='dachzeile').string
    title = '' if soup.find('span', class_='headline') is None else soup.find('span', class_='headline').string
    headline = dachzeile + ' - ' + title

    # TOPIC
    topic = '' if len(link.split("/")) < 3 else link.split("/")[3]

    # AUTHOR
    author = '' if soup.find('p', class_='autorenzeile') is None else soup.find('p', class_='autorenzeile').string
    author = author.replace("Von ", "")
    author = author.replace(",", "")

    # TEXT_BODY
    text_body = ''
    text_body_tag = soup.find_all('p', 'text')
    for ptag in text_body_tag:
        text_body = text_body + ptag.get_text()

    text_body = ' '.join(text_body.split())  # entfernt alle überschüssigen whitespaces und Zeilenumbrüche
    text_body = text_body.replace(creation_date, "")  # entfernt den Zeitstempel aus dem Text

    # CLEAN TIME
    creation_date = creation_date.replace("Stand: ", "")
    creation_date = creation_date.replace(" Uhr", "")

    return Article(headline, link, text_body, 'https://www.tagesschau.de', 'tagesschau', author, topic, date.today(),
                   creation_date)


# ************************* Flask web app *************************  #


app = Flask(__name__)


# Hier wird der Pfad(route) angegeben der den scraper arbeiten lässt.
# In dem Fall ist die URL "localhost:5000/pikio"
@app.route('/tagesschau')
def get_articles():
    links = get_news_links('http://www.tagesschau.de/xml/rss2')
    articles = []
    for link in links:
        print(link)
        articles.append(scrape(link))
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/')
def index():
    return "<h1>Go to 'localhost:5000/tagesschau</h1>"


# Web Application wird gestartet
if __name__ == '__main__':
    app.run()
