import requests
from bs4 import BeautifulSoup
import xplore
import os
import dotenv
import json


class Article:
    def __init__(self, title, url, abstract):
        self.url = url
        self.title = title
        self.abstract = abstract


class PageLink:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f"{self.title} ({self.url})"

    def get_article(self):
        return Article(self)


def is_article(article):
    try:
        int(article['start_page'])
        return True
    except ValueError:
        return False


def get_recently_added_articles():
    dotenv.load_dotenv()
    api_key = os.environ.get("IEEE_API_KEY")

    query = xplore.xploreapi.XPLORE(api_key)
    # query.articleTitle('Deep Learning')
    query.publicationTitle(
        'IEEE Transactions on Visualization and Computer Graphics')
    query.publicationYear('2023')
    data = query.callAPI()
    # print(data.decode('utf-8')[:100])
    js = json.loads(data.decode('utf-8'))
    # output to file
    # articles = js['articles']
    # with open('data.json', 'w', encoding='utf-8', errors='ignore') as outfile:
    #     json.dump(js, outfile)
    articles = []
    for article in js['articles']:
        if is_article(article):
            articles.append(
                Article(article['title'], article['html_url'], article['abstract']))
    # print(len(articles))
    return articles
    # try:
    #     start_page = int(article['start_page'])
    #     # print(article['start_page'])
    # except ValueError:
    #     print(article['title'])
    # print(articles[0]['title'])

    # print(js)

    # print("type", type(data))
    # print("len", len(data))
    # print(type(data[0]))
    # print(data[0])
    # print(data[1])
    # my_json = data.decode('utf8').replace("'", '"')
    # print(my_json)

#     url = "https://ieeexplore.ieee.org"
#     response = requests.get(url + "/xpl/tocresult.jsp?isnumber=4359476")
#     html = response.text
#     print(response)

#     soup = BeautifulSoup(html, "html.parser")

#     contents = soup.find("div", class_="issue-list-container")

#     if contents:
#         items = contents.find_all("div", class_="result-item")
#         page_links = []
#         for item in items:
#             a = item.find("a")
#             page_links.append(PageLink(a.text, url + a["href"]))
#         return page_links
#     else:
#         return []

# for link in get_recently_added_links():
#     print(link)


# get_recently_added_articles()
