import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, page_link):
        html = requests.get(page_link.url).text
        soup = BeautifulSoup(html, "html.parser")

        self.url = page_link.url
        self.title = self._get_title(soup)
        self.abstract = self._get_abstract(soup)

    def _get_title(self, soup):
        # NOTE: remove the prefix "Title:"
        return soup.find("h1", class_="title").text[6:]

    def _get_abstract(self, soup):
        # NOTE: remove the prefix "Abstract:  "
        return soup.find("blockquote", class_="abstract").text[11:]


class PageLink:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f"{self.title} ({self.url})"

    def get_article(self):
        return Article(self)


def get_recently_added_links():
    url = "https://arxiv.org"

    response = requests.get(url + "/list/cs.GR/recent")
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    contents = soup.find("div", id="dlpage")

    if contents:
        page_links = []
        for a in contents.find_all("a", title="Abstract"):
            page_links.append(PageLink(a.text, url + a["href"]))
        return page_links
    else:
        return []
