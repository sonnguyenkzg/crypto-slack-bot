# main.py
"""
Main script for the crypto wallet balance Slack bot.
Fetches USDT balances, logs data, generates trend charts, and sends reports to Slack.
Designed for scheduled execution (e.g., via cron).
"""

# Core Functionality Imports
from bot.usdt_checker import fetch_all_usdt_balances
from bot.csv_logger import log_to_csv
from bot.visualizer import plot_wallet_trends

# Configuration Imports
from bot.config import WALLETS, NUM_RECORDS_TO_PLOT, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID

# Slack API Client
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Standard Library Imports
from datetime import datetime, timezone, timedelta # <-- ADDED timezone, timedelta back for this purpose

def run_bot():
    """
    Executes the bot's full cycle: fetching balances, logging, plotting, and reporting.
    """
    # Get current time in GMT+7 for consistent logging of bot run times
    gmt7_now = datetime.now(timezone(timedelta(hours=7))) # <-- FIX: Use GMT+7 timezone for this print

    print(f"--- Bot Run Started: {gmt7_now.strftime('%Y-%m-%d %H:%M:%S')} ---") # <-- Uses GMT+7

    # Initialize variables to ensure they exist even if early steps fail
    message = ""
    balances = {}
    image_path = None
    slack_client = None

    # --- 1. Fetch Balances ---
    try:
        message, balances = fetch_all_usdt_balances()
        print("✅ Balances fetched successfully.")
    except Exception as e:
        print(f"❌ Error fetching balances: {e}")
        message = f"❌ Error fetching USDT balances: {e}" 

    # --- 2. Save to CSV ---
    try:
        log_to_csv(WALLETS, balances)
        print("✅ Balances logged to CSV.")
    except Exception as e:
        print(f"❌ Error logging balances to CSV: {e}")

    # --- 3. Generate Chart ---
    try:
        image_path = plot_wallet_trends() 
        print("✅ Chart generated successfully.")
    except Exception as e:
        print(f"❌ Error generating chart: {e}")

    # --- 4. Prepare and Send Report to Slack ---
    if SLACK_BOT_TOKEN and SLACK_CHANNEL_ID:
        try:
            slack_client = WebClient(token=SLACK_BOT_TOKEN)
            
            final_slack_text_message = message + f"\n\n📈 *Wallet Balance Trend* (last {NUM_RECORDS_TO_PLOT} records)"
            
            slack_client.chat_postMessage(
                channel=SLACK_CHANNEL_ID,
                text=final_slack_text_message
            )
            print("✅ USDT Text report sent to Slack.")
        except SlackApiError as e:
            print(f"❌ Slack Text Error: {e.response['error']}")
        except Exception as e:
            print(f"❌ Unexpected error sending text to Slack: {e}")

        # --- 5. Upload Chart via bot ---
        if slack_client and image_path:
            try:
                slack_client.files_upload_v2(
                    channel=SLACK_CHANNEL_ID,
                    initial_comment="",
                    file=image_path,
                    filename="",
                    title=""
                )
                print("✅ Chart image uploaded to Slack.")
            except SlackApiError as e:
                print(f"❌ Slack API Error uploading chart: {e.response['error']}")
            except Exception as e:
                print(f"❌ Unexpected error uploading chart: {e}")
        elif not image_path:
            print("ℹ️ Chart not generated, skipping upload.")
    else:
        print("ℹ️ Slack bot token or channel ID not configured. Skipping Slack reporting.")

    # Get current time in GMT+7 for consistent logging of bot run times
    gmt7_end_now = datetime.now(timezone(timedelta(hours=7))) # <-- FIX: Use GMT+7 timezone for this print
    print(f"--- Bot Run Finished: {gmt7_end_now.strftime('%Y-%m-%d %H:%M:%S')} ---") # <-- Uses GMT+7

# --- Entry Point ---
if __name__ == "__main__":
    run_bot()