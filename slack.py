import egdl
import summarize
import post
import tog
import datetime

def check_new_articles(title, posted_articles_file):
    posted_articles = []
    with open(posted_articles_file, "r") as f:
        for line in f:
            posted_articles.append(line.strip())
    
    if title in posted_articles:
        return False
    else:
        # add title to posted_articles
        with open(posted_articles_file, "a") as f:
            f.write(title + "\n")
        return True

def execute(page_links, message_prefix, posted_articles_file, channel):
    new_articles = []
    for page_link in page_links:
        if check_new_articles(page_link.title, posted_articles_file):
            article = page_link.get_article()
            new_articles.append(article)
        
    if new_articles != []:
        message = f"{message_prefix}\n"
        article = new_articles[0]
        summary = summarize.summarize(article.title, article.abstract)
        message += f"\n<{article.url}|{article.title}>\n{summary}\n"
        post.post_message(message, channel)

        for article in new_articles[1:]:
            summary = summarize.summarize(article.title, article.abstract)
            message += f"\n<{article.url}|{article.title}>\n{summary}\n"
            post.post_message(message, channel)

def main():
    try:
        with open("log.txt", "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n"
            f.write("Scheduled task started at " + timestamp)

        execute(egdl.get_recently_added_links(), 
                "EGに新しい論文が追加されました！", 
                "posted_articles_eg.txt",
                "#new-papers-bot")
        
        execute(tog.get_recently_added_links(), 
                "ToGに新しい論文が追加されました！", 
                "posted_articles_tog.txt",
                "#new-papers-bot")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
