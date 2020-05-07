from bs4 import BeautifulSoup
import requests
from datetime import date
import article


def get_news_links(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    item = soup.find_all('div', class_='news-titlelead-wrapper')

    links = []
    for item in item:
        if item.find('a'):
            link = item.find('a').get('href').strip()
            if not "wprost.pl" in link:
                link = "https://www.wprost.pl" + link
            links.append(link)
    return links


def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    # HEADLINE
    headline = soup.find('h1').string

    # TOPIC
    topic = ''
    if len(soup.find_all('span', class_='item-containers')) > 0:
        topic = soup.find_all('span', class_='item-containers')[0].find('a').get('a')

    topic = "" if topic is None else topic

    # AUTHOR
    author = ''
    if len(soup.find_all('span', class_='source')) > 0:
        author = soup.find_all('span', class_='source')[0].get_text()

    # TEXT_BODY
    if len(soup.find_all('div', 'art-text-inner')) > 0:
        text_body = soup.find_all('div', 'art-text-inner')[0].get_text()
        text_body = ' '.join(text_body.split())
    else:
        text_body = ''

    # CREATION_DATE
    creation_date = ''
    if soup.find('time'):
        creation_date = soup.find('time').get('datetime')

    return article.Article(headline.strip(), link, text_body, 'https://www.wprost.pl', 'wprost', author.strip(), topic.strip(), date.today(), creation_date)
