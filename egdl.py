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
        description = soup.find("div", class_="simple-item-view-description")
        if description:
            abstract = description.find("div")
            return abstract.text
        else:
            return ""
    
    def _get_authors(self, soup):
        authors = []
        author_elements = soup.find_all("div", class_="ds-dc_contributor_author-authority")
        for author_element in author_elements:
            authors.append(author_element.text)
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
    # URLを指定
    url = "https://diglib.eg.org"

    # URLからHTMLを取得
    response = requests.get(url)
    html = response.text

    # HTMLを解析してタイトルを取得
    soup = BeautifulSoup(html, "html.parser")

    recently_added_section = soup.find("h2", string="Recently Added")

    if recently_added_section:
        # "Recently Added"セクションの次の<ul>要素を取得
        list_element = recently_added_section.find_next("ul")
        
        # <ul>要素内のすべての<li>要素を取得
        page_links = []
        list_items = list_element.find_all("li")
        for item in list_items:
            a = item.find("a")
            page_links.append(PageLink(a.text, url + a["href"]))
        return page_links
    else:
        return []

def search(query):
    url = "https://diglib.eg.org"
    
    query = query.replace(" ", "+")
    result_url = f"https://diglib.eg.org/discover?scope=%2F&query={query}&submit="
    response = requests.get(result_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # get all ds-artifact-item
    items = soup.find_all("div", class_="ds-artifact-item")
    page_links = []
    for item in items:
        a = item.find("a")
        h4 = item.find("h4")
        page_links.append(PageLink(h4.text, url + a["href"]))
    return page_links
