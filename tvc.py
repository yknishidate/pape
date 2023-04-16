import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, page_link):
        html = requests.get(page_link.url).text
        soup = BeautifulSoup(html, "html.parser")

        self.url = page_link.url
        self.title = self._get_title(soup)
        self.abstract = self._get_abstract(soup)
        self.authors = []

    def _get_title(self, soup):
        return soup.find("h1", class_="c-article-title").text

    def _get_abstract(self, soup):
        section = soup.find("div", id="Abs1-content")
        if section:
            abstract = section.find("p")
            return abstract.text
        else:
            return ""


class PageLink:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f"{self.title} ({self.url})"

    def get_article(self):
        return Article(self)


def get_recently_added_links():
    url = "https://www.springer.com/journal/371"

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    titles = soup.find_all("h3", class_="c-card__title")
    page_links = []
    for title in titles:
        a = title.find("a")
        page_links.append(PageLink(a.text, a["href"]))
    return page_links
