import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, page_link):
        html = requests.get(page_link.url).text
        soup = BeautifulSoup(html, "html.parser")

        self.url = page_link.url
        self.title = self._get_title(soup)
        self.abstract = self._get_abstract(soup)
        self.authors = self._get_authors(soup)

    def _get_title(self, soup):
        return soup.find("h1", class_="citation__title").text

    def _get_abstract(self, soup):
        section = soup.find("div", class_="abstractSection")
        if section:
            abstract = section.find("p")
            return abstract.text
        else:
            return ""

    def _get_authors(self, soup):
        authors = []
        authors_names = soup.find_all("span", class_="loa__author-name")
        for name in authors_names:
            authors.append(name.text)
        return authors


class PageLink:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f"{self.title} ({self.url})"

    def get_article(self):
        return Article(self)


def get_recently_added_links():
    url = "https://dl.acm.org"

    response = requests.get(url + "/toc/pacmcgit/current")
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    contents = soup.find("div", id="tableOfContent")

    if contents:
        titles = contents.find_all("h5", class_="issue-item__title")
        page_links = []
        for title in titles:
            a = title.find("a")
            page_links.append(PageLink(a.text, url + a["href"]))
        return page_links
    else:
        return []
