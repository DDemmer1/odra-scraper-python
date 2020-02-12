#!/usr/bin/python
# -*- coding: utf-8 -*-
import tagesschau
import wprost
import germantimes
import blanas
import time
import bbc
import superexpress
import theeuropean
import warsawvoice
import rotefahnepolsat

from flask import Flask, jsonify, url_for

app = Flask(__name__)


@app.route('/tagesschau')
def get_articles_tagesschau():
    links = tagesschau.get_news_links('http://www.tagesschau.de/xml/rss2')
    articles = []
    for link in links:
        articles.append(tagesschau.scrape(link))
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/wprost')
def get_articles_wprost():
    links = wprost.get_news_links('https://www.wprost.pl/')
    articles = []
    for link in links:
        articles.append(tagesschau.scrape(link))
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/german-times')
def get_articles_german_times():
    links = germantimes.get_news_links('http://www.german-times.com')
    articles = []
    for link in links:
        articles.append(germantimes.scrape(link))
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/blaetter')
def get_articles_blaetter():
    link_data = blanas.get_news_links('https://www.blaetter.de/rss.xml')
    articles = []
    for link in link_data:
        articles.append(blanas.scrape(link['link'], link['creation_date']))
    return jsonify([e.serialize() for e in articles])


@app.route('/naszdziennik')
def get_articles_nd():
    link_data = blanas.get_news_links('https://naszdziennik.pl/articles/rss.xml')
    articles = []
    for link in link_data:
        articles.append(blanas.scrape(link['link']))
    return jsonify([e.serialize() for e in articles])


@app.route('/bbc')
def get_articles_bbc():
    links = bbc.get_news_links('http://feeds.bbci.co.uk/news/rss.xml')
    articles = []
    for link in links:
        if bbc.scrape(link):
            articles.append(bbc.scrape(link))
        time.sleep(.5)
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/super-express')
def get_articles_super_express():
    links = superexpress.get_news_links('https://www.se.pl/najnowsze/')
    articles = []
    for link in links:
        articles.append(superexpress.scrape(link))
        time.sleep(.5)
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/theeuropean')
def get_articles_theeuropean():
    links = theeuropean.get_news_links('https://www.theeuropean.de/')
    articles = []
    for link in links:
        articles.append(theeuropean.scrape(link))
    return jsonify([e.serialize() for e in articles])


@app.route('/warsawvoice')
def get_articles_pol():
    links = warsawvoice.get_news_links('http://www.warsawvoice.pl')
    articles = []
    for link in links:
        articles.append(warsawvoice.scrape(link))
    return jsonify([e.serialize() for e in articles])  # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/polsatnews')
def get_articles_polsatnews():
    scraped_articles = []
    # Artikellinks finden
    links = rotefahnepolsat.get_links('https://www.polsatnews.pl/')
    for link in links:
        # print(str(link)+"\n")
        article = rotefahnepolsat.scrape(link)
        scraped_articles.append(article)
    return jsonify([e.serialize() for e in scraped_articles])
    # jsonify erzeugt aus einem Objekt einen String im JSON Format


@app.route('/rotefahne')
def get_articles_rotefahne():
    scraped_articles = []
    # Artikellinks finden
    links = rotefahnepolsat.get_links('https://rotefahne.eu/')
    for link in links:
        # print(str(link)+"\n")
        article = rotefahnepolsat.scrape(link)
        scraped_articles.append(article)
    return jsonify([e.serialize() for e in scraped_articles])
    # jsonify erzeugt aus einem Objekt einen String im JSON Format


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if url != "/":
                links.append(url)
    return jsonify(links)


# Web Application wird gestartet
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8081)
