# bot/config.py
"""
Configuration settings for the crypto Slack bot.
Environment variables and system settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Slack API Credentials ---
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # For Socket Mode

# --- API Configuration ---
API_TIMEOUT = 10  # seconds for API requests
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # Official USDT TRC20 contract

# --- File Paths ---
WALLETS_FILE = "wallets.json"
CSV_FILE = "wallet_balances.csv"

# --- Timezone ---
GMT_OFFSET = 7  # GMT+7 timezone offset

# --- Access Control ---
# List of Slack User IDs who are authorized to use interactive commands.
# To find a user's ID: In Slack, right-click on their name -> "Copy Link" or "View Profile"
# The ID typically starts with 'U' followed by alphanumeric characters (e.g., "U123ABCDE").
ALLOWED_SLACK_USERS = [
    "U0904UHELTE",
    "U090GBUM3HV"
]