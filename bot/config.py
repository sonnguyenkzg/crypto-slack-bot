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