from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = "C090FM0PN0Z"
IMAGE_PATH = "wallet_trend.png"

client = WebClient(token=SLACK_TOKEN)

try:
    response = client.files_upload_v2(
        channel=CHANNEL_ID,
        initial_comment="📊 Wallet Balance Trend",
        file=IMAGE_PATH,
        title="Daily TRX Wallet Report"
    )
    if response["ok"]:
        print("✅ Image uploaded to Slack successfully")
except SlackApiError as e:
    print(f"❌ Slack API Error: {e.response['error']}")
