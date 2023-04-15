import os
import sys
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import dotenv
import summarize
import egdl
import tog
import log

dotenv.load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


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

app = App(token=SLACK_BOT_TOKEN)


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")
    log.log("Hello!")


def get_url(element):
    if element['type'] == 'link':
        return element['url']
    if 'elements' not in element:
        return None
    for child in element['elements']:
        url = get_url(child)
        if url is not None:
            return url
    return None


@app.message("summarize")
def message_summarize(message, say):
    for block in message['blocks']:
        url = get_url(block)
        if 'acm.org' in url:
            page_link = tog.PageLink("", url)
            article = page_link.get_article()
            log.log("Summarized " + article.title)
            summary = summarize.summarize(article.title, article.abstract)
            msg = f"\n<{article.url}|{article.title}>\n{summary}"
            say(msg)


if __name__ == "__main__":
    try:
        if sys.argv[1] == "serve":
            log.log("App started")
            SocketModeHandler(app, SLACK_APP_TOKEN).start()
        elif sys.argv[1] == "post":
            log.log("Posted new papers")
            execute(egdl.get_recently_added_links(), 
                    "EGに新しい論文が追加されました！", 
                    "posted_articles_eg.txt",
                    "#new-papers-bot")
            
            execute(tog.get_recently_added_links(), 
                    "ToGに新しい論文が追加されました！", 
                    "posted_articles_tog.txt",
                    "#new-papers-bot")
    except Exception as e:
        log.log("Error: " + str(e))
