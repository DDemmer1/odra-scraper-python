#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from datetime import date
import article


def get_links(url):
    relevant_links = []
    user_agent = {'User-agent': 'Mozilla/5.0'}
    result = requests.get(url, headers=user_agent)
    # Code 200?
    # print(result.status_code)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    if "rotefahne.eu" in url:
        newstags = soup.find_all('td')
        for element in newstags:
            if element.find('a'):
                link = (element.find('a').get('href'))
                if "/RoteFahne.eu" in link:
                    relevant_links.append(link)
        return relevant_links

    elif "polsatnews.pl" in url:
        newstags = soup.find_all('article', class_='news')
        for element in newstags:
            if element.find('a'):
                # class = "news_link" in href
                link = (element.find('a').get('href'))
                # Tochterseiten (z.B. Sport) ausschliessen:
                if "polsatnews" in link:
                    relevant_links.append(link)
        return relevant_links


def scrape(link):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    soup = BeautifulSoup(requests.get(link, headers=user_agent).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    if "RoteFahne.eu" in link:
        # HEADLINE
        headline = soup.find('h1', class_='title').string
        # print(headline)

        # TOPIC
        topic = ''
        # extrahiert topic aus bradcrumbs:
        category_tag = soup.find('span', class_='category')
        topic = [element.string for element in category_tag.find_all('a')][0]
        # print(topic)

        # AUTHOR
        match = soup.find('a', class_='unter')
        if match is not None:
            author = match.string.lstrip()
        else:
            author = "unknown"
        # print(author)

        # TEXT_BODY
        text = ''
        text_body = soup.find('div', {'class': 'column'}).findAll('p')
        for element in text_body:
            text += '\n' + ''.join(element.find_all(text=True))
        # print(text)

        # CREATION_DATE
        creation_date = soup.find('span', class_="date").string
        # print(creation_date)

        return article.Article(headline.strip(), link, text.strip().replace("/.dropcap ", ""), 'https://rotefahne.eu/', 'rotefahne', author, topic,
                       date.today(), creation_date)

    elif "polsatnews.pl" in link:
        # HEADLINE
        headline = ''
        if link.find('news__title'):
            # Ausschluss von Artikeln anderer Seiten (mit anderen Themen (ueberwiegend Sport) und HTML-Tags)
            headline = soup.find('h1', class_='news__title').string
            # print(headline)

        # TOPIC
        topic = soup.find_all('a', class_='breadcrumb__link')[-1].string
        # print(topic)

        # AUTHOR
        match = soup.find('div', class_='news__author')
        if match is not None:
            author = match.string
        else:
            author = "unknown"
        # print(author)

        # TEXT_BODY
        text_body = soup.find_all('div', class_='news__description')[0].get_text()
        text_body = ' '.join(text_body.split())  # entfernt alle ueberschuessigen whitespaces und Zeilenumbrueche
        # print(text_body)

        # CREATION_DATE
        creation_date = str()
        if soup.find('time', class_="news__time"):
            creation_date = soup.find('time').get('datetime')
            # print(creation_date)

        return article.Article(headline, link, text_body, 'https://www.polsatnews.pl/', 'polsatnews', author,
                       topic, date.today(), creation_date)