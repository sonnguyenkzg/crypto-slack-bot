from bot.usdt_checker import fetch_all_usdt_balances
from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

message, balances = fetch_all_usdt_balances()

print(message)

# Optional: send to Slack
if SLACK_BOT_TOKEN and SLACK_CHANNEL_ID:
    client = WebClient(token=SLACK_BOT_TOKEN)
    client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
