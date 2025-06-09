# main.py
"""
Main script for the crypto wallet balance Slack bot.
Fetches USDT balances, logs data, and sends text reports to Slack.
Designed for scheduled execution (e.g., via cron).
"""
from datetime import datetime, timezone, timedelta

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from bot.config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, GMT_OFFSET
from bot.usdt_checker import fetch_all_usdt_balances, get_wallets_for_checking
from bot.csv_logger import log_to_csv


def run_bot():
    """
    Executes the bot's full cycle: fetching balances, logging, and reporting.
    """
    # Get current time in GMT+7
    gmt_now = datetime.now(timezone(timedelta(hours=GMT_OFFSET)))
    print(f"--- Bot Run Started: {gmt_now.strftime('%Y-%m-%d %H:%M:%S')} GMT+{GMT_OFFSET} ---")

    # Load wallets
    wallets = get_wallets_for_checking()
    if not wallets:
        print("❌ No wallets found")
        return
    
    print(f"📊 Loaded {len(wallets)} wallets")

    # Initialize variables
    message = ""
    balances = {}

    # --- 1. Fetch Balances ---
    try:
        message, balances = fetch_all_usdt_balances()
        print("✅ Balances fetched successfully")
    except Exception as e:
        print(f"❌ Error fetching balances: {e}")
        message = f"❌ Error fetching USDT balances: {e}"

    # --- 2. Save to CSV ---
    try:
        log_to_csv(wallets, balances)
        print("✅ Balances logged to CSV")
    except Exception as e:
        print(f"❌ Error logging balances to CSV: {e}")

    # --- 3. Send Text Report to Slack ---
    if SLACK_BOT_TOKEN and SLACK_CHANNEL_ID:
        try:
            slack_client = WebClient(token=SLACK_BOT_TOKEN)
            slack_client.chat_postMessage(
                channel=SLACK_CHANNEL_ID,
                text=message
            )
            print("✅ Text report sent to Slack")
        except SlackApiError as e:
            print(f"❌ Slack Error: {e.response['error']}")
        except Exception as e:
            print(f"❌ Unexpected error sending to Slack: {e}")
    else:
        print("ℹ️ Slack credentials not configured. Skipping Slack reporting")

    # Finish
    gmt_end = datetime.now(timezone(timedelta(hours=GMT_OFFSET)))
    print(f"--- Bot Run Finished: {gmt_end.strftime('%Y-%m-%d %H:%M:%S')} GMT+{GMT_OFFSET} ---")


if __name__ == "__main__":
    run_bot()