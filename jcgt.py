import json
import requests


class Article:
    def __init__(self, title, url, abstract):
        self.url = url
        self.title = title
        self.abstract = abstract


def get_recently_added_articles():
    url = 'https://jcgt.org/papers.json'

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        print(f"Failed to fetch JSON data: {url}")

    articles = []
    latest_volume_index = len(data) - 1
    latest_volume = data[latest_volume_index]

    issues = latest_volume['issues']
    latest_issue_index = len(issues) - 1
    latest_issue = issues[latest_issue_index]
    latest_papers = latest_issue['papers']

    for index, paper in enumerate(latest_papers):
        volume_str = str(latest_volume_index + 1).zfill(4)
        issue_str = str(latest_issue_index + 1).zfill(2)
        index_str = str(index + 1).zfill(2)
        url = f"https://jcgt.org/published/{volume_str}/{issue_str}/{index_str}/"
        articles.append(Article(paper['title'], url, paper['abstractText']))
    return articles
