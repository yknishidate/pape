import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import dotenv
import summarize
import tog
import post

dotenv.load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

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
            summary = summarize.summarize(article.title, article.abstract)
            msg = f"\n<{article.url}|{article.title}>\n{summary}"
            say(msg)

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
