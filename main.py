# main.py
"""
Send daily !check report to Slack at noon GMT+7
"""
from slack_sdk import WebClient
from bot.config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID
from bot.slack_commands import handle_check_command
import re

def fix_slack_formatting(text):
    """Fix markdown formatting for scheduled messages to match !check exactly"""
    # Add bold title at the top
    text = ":moneybag: *Daily Balance Report*\n\n" + text
    
    # Fix Time line: **Time:** -> *Time:*
    text = re.sub(r'\*\*Time:\*\*', '*Time:*', text)
    
    # Fix Total line: **Total:** -> *Total:*
    text = re.sub(r'\*\*Total:\*\*', '*Total:*', text)
    
    # Fix wallet names: `wallet_name`: **amount** -> `wallet_name`: amount
    text = re.sub(r'`([^`]+)`:\s*\*\*([^*]+)\*\*', r'`\1`: \2', text)
    
    return text

def run_bot():
    # Get the exact same output as !check command
    message = handle_check_command("")
    
    # Fix formatting for scheduled messages
    formatted_message = fix_slack_formatting(message)
    
    # Send to Slack
    if SLACK_BOT_TOKEN and SLACK_CHANNEL_ID:
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        slack_client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=formatted_message
        )
        print("✅ Daily report sent to Slack")
    else:
        print("❌ Slack credentials not configured")

if __name__ == "__main__":
    run_bot()