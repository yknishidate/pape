from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import dotenv
import os

dotenv.load_dotenv()

SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

def post_message(message, channel):
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        print(f"Message posted: {response['ts']}")
    except SlackApiError as e:
        print(f"Error posting message: {e}")
