from bs4 import BeautifulSoup
import requests
from datetime import date
import feedparser
import article

# Sucht sich die eine Liste mit allen Artikel links zusammen
def get_news_links(url):
    links = []
    data = feedparser.parse('http://www.tagesschau.de/xml/rss2')
    for item in data.entries:
        if 'livestream' not in item.link:
            if 'tagesschau' in item.link:
                links.append(item.link)
    return links


# Extrahiert alle notwendigen informationen von einem einzigen Artikel
def scrape(link):
    try:
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
        if text_body is not '':
            text_body = ' '.join(text_body.split())  # entfernt alle überschüssigen whitespaces und Zeilenumbrüche
            text_body = text_body.replace(creation_date, "")  # entfernt den Zeitstempel aus dem Text

        # CLEAN TIME
        creation_date = creation_date.replace("Stand: ", "")
        creation_date = creation_date.replace(" Uhr", "")

        return article.Article(headline, link, text_body, 'https://www.tagesschau.de', 'tagesschau', author, topic, date.today(), creation_date)
    except AttributeError:
        print("AttributeError")