import egdl
import summarize
import tog
import log
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import dotenv
import os

dotenv.load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

def post_message(message, channel):
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        print(f"Message posted: {response['ts']}")
    except SlackApiError as e:
        print(f"Error posting message: {e}")


def check_new_articles(title, posted_articles_file):
    posted_articles = []
    with open(posted_articles_file, "r") as f:
        for line in f:
            posted_articles.append(line.strip())
    
    if title in posted_articles:
        return False
    else:
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
        post_message(message, channel)

        for article in new_articles[1:]:
            summary = summarize.summarize(article.title, article.abstract)
            message += f"\n<{article.url}|{article.title}>\n{summary}\n"
            post_message(message, channel)

def main():
    try:
        log.log("Checking for new articles...")

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
