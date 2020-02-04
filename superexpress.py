from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timezone
import article


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    items = soup.find_all('div', class_='element__media')

    links = []
    maxItems = 20
    counter = 0
    for item in items:
        if counter <= maxItems:
            if item.find('a').get('href').startswith('//'):
                links.append("https:" + item.find('a').get('href').strip())
            else:
                links.append(item.find('a').get('href').strip())
        counter += 1
    return links


def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    # HEADLINE
    headline = soup.find('h1').string
    #headline = soup.find('div', class_='title').string

    # TOPIC
    topic = ''
    #if len(soup.find_all('div', class_='breadcrumbs')) > 0:
    #topic = soup.find_all('div', class_='breadcrumbs')[0].find_all('a')[1].get('title')
    #topic = soup.find("a", class_="active").get_text()

    # AUTHOR
    author = ''
    if soup.find('meta', itemprop='name'):
        author = soup.find('meta', itemprop='name').get('content')

    # TEXT_BODY
    text_body = soup.find_all('div', 'gl_plugin article')[0].get_text()
    text_body = ' '.join(text_body.split())  # entfernt alle überschüssigen whitespaces und Zeilenumbrüche

    # CREATION_DATE
    creation_date = ''
    #if soup.find('time'):
    #    creation_date = soup.find('time').get('datetime')

    if soup.find('meta', itemprop ='datePublished'):
        creation_date =  soup.find('meta', itemprop ='datePublished').get('content')

    # CRAWL_DATE
    crawl_date = datetime.now()

    return article.Article(headline, link, text_body, 'https://www.se.pl', 'super-express', author, topic, crawl_date, creation_date)
