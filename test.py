from bot.balance_checker import get_trx_balance
from bot.csv_logger import log_to_csv
from bot.visualizer import plot_wallet_trends
from bot.config import WALLETS
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timezone, timedelta
import os

# === 1. Load env ===
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# === 2. Get balances ===
balances = {name: get_trx_balance(addr) for name, addr in WALLETS.items()}

# === 3. Send text summary via bot token ===
if SLACK_BOT_TOKEN and SLACK_CHANNEL_ID:
    client = WebClient(token=SLACK_BOT_TOKEN)

    gmt7_now = datetime.now(timezone(timedelta(hours=7)))
    time_str = gmt7_now.strftime("%Y-%m-%d %H:%M")

    lines = [f"\n *📢 KZP Wallet Balances (TRX)*", f"_As of {time_str} GMT+7_"]
    lines.append("")  

    for name, value in balances.items():
        lines.append(f"- `{name}`: *{value:.2f} TRX*")
    lines.append("")
    lines.append("")
    lines.append("📈 *Wallet Balance Trend* (last 13 records)")
    message = "\n".join(lines)

    try:
        client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=message
        )
        print("✅ Text report sent via bot")
    except SlackApiError as e:
        print(f"❌ Slack Text Error: {e.response['error']}")

# === 4. Save to CSV ===
log_to_csv(WALLETS, balances)

# === 5. Generate chart only (not upload!) ===
image_path = plot_wallet_trends()

# === 6. Upload chart via bot ===
try:
    response = client.files_upload_v2(
    channel=SLACK_CHANNEL_ID,
    initial_comment="",
    file=image_path,
    filename="",   # ⬅️ Hide filename preview
    title=""       # ⬅️ Hide header above the image
    )
    if response["ok"]:
        print("✅ Chart image uploaded to Slack")
except SlackApiError as e:
    print(f"❌ Slack API Error: {e.response['error']}")
