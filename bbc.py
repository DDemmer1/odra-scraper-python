from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timezone
import article
import feedparser


def get_news_links(url):
    links = []
    data = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')
    for item in data.entries:
        links.append(item.link)
    return links


# Extrahiert alle notwendigen informationen von einem einzigen Artikel
def scrape(link):
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')
    [s.extract() for s in soup('script')]  # entfernt alle script tags

    # HEADLINE
    headline = soup.find('h1').string

    # TOPIC
    topic = ''
    if soup.find("a", class_="navigation-wide-list__link navigation-arrow--open"):
        menuActive = soup.find("a", class_="navigation-wide-list__link navigation-arrow--open")
        topic = menuActive.find("span").get_text()

    # AUTHOR
    author = ''
    if soup.find('span', class_='byline__name'):
        author = soup.find('span', class_='byline__name').get_text()

    # TEXT_BODY
    if soup.find('div', class_='story-body__inner'):
        innerArticle = soup.find('div', class_='story-body__inner')
    elif soup.find('div', class_='vxp-media__summary'):
        innerArticle = soup.find('div', class_='vxp-media__summary')
    else:
        print ("no content found on" + link)
        return

    pList = innerArticle.find_all('p')

    text_body = ''
    for p in pList:
        text_body += p.get_text() + ' '

    # CREATION_DATE
    creation_date = ''

    #soup.find('div', class_='date date--v2 relative-time').get('data-datetime')
    if soup.find('div', class_='date date--v2 relative-time'):
        timeStamp = soup.find('div', class_='date date--v2 relative-time').get('data-seconds')
        creation_date = datetime.fromtimestamp(timeStamp, timezone.utc)
        #creation_date = datetime.fromtimestamp(timeStamp).strftime("%A, %B %d, %Y %I:%M:%S")

    # CRAWL_DATE
    crawl_date = datetime.now()

    return article.Article(headline, link, text_body, 'https://www.bbc.com', 'bbc', author, topic, crawl_date, creation_date)
