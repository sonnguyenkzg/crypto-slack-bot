# bot/config.py
"""
Configuration settings for the crypto Slack bot.
Centralizes API keys, wallet addresses, and operational parameters.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Wallet Configuration ---
WALLETS = {
    "KZP TH Y 1": "TSpAswScHnu6WqJDaZzjWEA4ztPSzPRtPZ",
    "KZP TH BM 1": "TS928hvaYDoGNhzYJcvyDSL2EB6XjPUyTh",
    "KZP PH 1": "THB5JtMUtvmZ94HdCqqL34SzSfJavF58Ga",
    "KZP PH BM 1": "TTRpG11vBzdir9GcD4MmkUNoubGxJUpwsf"
}

# --- Slack API Credentials (fetched from environment variables) ---
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
# SLACK_WEBHOOK_URL is removed as it's not used by WebClient.
# If you plan to use webhooks later, you can add it back.

# --- Plotting Configuration ---
NUM_RECORDS_TO_PLOT = 13 # Number of historical data points to include in the trend chart