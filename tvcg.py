import requests
from bs4 import BeautifulSoup

class Article:
    def __init__(self, page_link):
        html = requests.get(page_link.url).text
        soup = BeautifulSoup(html, "html.parser")

        self.title = page_link.title
        self.url = page_link.url
        self.abstract = self._get_abstract(soup)
        self.authors = self._get_authors(soup)

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
    url = "https://ieeexplore.ieee.org"
    response = requests.get(url + "/xpl/tocresult.jsp?isnumber=4359476")
    html = response.text
    print(response)

    soup = BeautifulSoup(html, "html.parser")

    contents = soup.find("div", class_="issue-list-container")

    if contents:
        items = contents.find_all("div", class_="result-item")
        page_links = []
        for item in items:
            a = item.find("a")
            page_links.append(PageLink(a.text, url + a["href"]))
        return page_links
    else:
        return []

for link in get_recently_added_links():
    print(link)

