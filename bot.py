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
import jcgt
import log
import cgit
import tvc
import tvcg
import arxiv

dotenv.load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


def post_message(message, channel, image_url=None):
    client = WebClient(token=SLACK_BOT_TOKEN)
    attachments = None
    if image_url:
        attachments = [
            {
                "fallback": "Image preview",
                "image_url": image_url,
            }
        ]

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message,
            attachments=attachments
        )
        print(f"Message posted: {response['ts']}")
    except SlackApiError as e:
        print(f"Error posting message: {e}")


def check_new_articles(page_link, posted_articles_file):
    posted_articles = []
    with open(posted_articles_file, "r", encoding='utf-8', errors='ignore') as f:
        for line in f:
            posted_articles.append(line.strip())

    if page_link.url in posted_articles:
        return False
    else:
        with open(posted_articles_file, "a", encoding='utf-8', errors='ignore') as f:
            f.write(page_link.url + "\n")
        return True


def format_message(article, summary):
    return f"\n*{article.title}*\n{summary}\n{article.url}\n"
    # return f"\n{summary}\n{article.url}\n"


def post_articles(articles, message_prefix, channel):
    if articles != []:
        message = f"{message_prefix}\n"

        # Add the first article
        article = articles[0]
        summary = summarize.summarize(article.title, article.abstract)
        message += format_message(article, summary)
        post_message(message, channel)

        # Add the rest of the articles
        for article in articles[1:]:
            summary = summarize.summarize(article.title, article.abstract)
            message = format_message(article, summary)
            post_message(message, channel)


def get_new_articles(page_links, posted_articles_file):
    new_articles = []
    for page_link in page_links:
        if check_new_articles(page_link, posted_articles_file):
            article = page_link.get_article()
            new_articles.append(article)
    return new_articles


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

            try:
                new_articles = get_new_articles(
                    egdl.get_recently_added_links(), "posted_articles_eg.txt")
                post_articles(new_articles, "EGに新しい論文が追加されました！",
                              "#new-papers-bot")
            except Exception as e:
                log.log("[EG] Error: " + str(e))

            try:
                new_articles = get_new_articles(
                    tog.get_recently_added_links(), "posted_articles_tog.txt")
                post_articles(new_articles, "ToGに新しい論文が追加されました！",
                              "#new-papers-bot")
            except Exception as e:
                log.log("[ToG] Error: " + str(e))

            try:
                new_articles = get_new_articles(
                    cgit.get_recently_added_links(), "posted_articles_cgit.txt")
                post_articles(new_articles, "CGITに新しい論文が追加されました！",
                              "#new-papers-bot")
            except Exception as e:
                log.log("[CGIT] Error: " + str(e))

            try:
                new_articles = get_new_articles(
                    tvc.get_recently_added_links(), "posted_articles_tvc.txt")
                post_articles(new_articles, "TVCに新しい論文が追加されました！",
                              "#new-papers-bot")
            except Exception as e:
                log.log("[TVC] Error: " + str(e))

            try:
                articles = jcgt.get_recently_added_articles()
                new_articles = [article for article in articles if check_new_articles(
                    article.title, "posted_articles_jcgt.txt")]
                post_articles(new_articles, "JCGTに新しい論文が追加されました！",
                              "#new-papers-bot")
            except Exception as e:
                log.log("[JCGT] Error: " + str(e))

            try:
                articles = tvcg.get_recently_added_articles()
                new_articles = [article for article in articles if check_new_articles(
                    article.title, "posted_articles_tvcg.txt")]
                post_articles(new_articles, "TVCGに新しい論文が追加されました！",
                              "#new-papers-bot")
            except Exception as e:
                log.log("[TVCG] Error: " + str(e))

            try:
                new_articles = get_new_articles(
                    arxiv.get_recently_added_links(), "posted_articles_arxiv_gr.txt")
                print(new_articles)
                post_articles(
                    new_articles, "arXiv/csGRに新しい論文が追加されました！", "#new-arxiv-gr")
            except Exception as e:
                log.log("[arXiv] Error: " + str(e))

    except Exception as e:
        log.log("Error: " + str(e))
