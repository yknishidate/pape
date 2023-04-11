import egdl

# Get the most recent articles
page_links = egdl.get_recently_added_links()
for page_link in page_links:
    print("Link:", page_link)
    article = page_link.get_article()
    print("Title:", article.title)
    print("Abstract:", article.abstract)
    print("Authors:", article.authors)
    print()

# Search for articles
page_links = egdl.search("deep learning")
for page_link in page_links:
    print("Link:", page_link)
    print()
