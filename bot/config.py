# bot/config.py
"""
Configuration settings for the crypto Slack bot.
Environment variables and system settings.
"""
import os
import subprocess

# Force load secure secrets IMMEDIATELY when module is imported
def _load_secure_secrets():
    """Load secrets from secure location if available"""
    secure_config_path = "/opt/usdt-bot-secrets/config"
    
    if os.path.exists(secure_config_path):
        try:
            # Read the secure config file
            result = subprocess.run(
                ["sudo", "cat", secure_config_path], 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=5
            )
            
            # Parse and set environment variables
            for line in result.stdout.strip().split('\n'):
                if line.startswith('export ') and 'SLACK_' in line:
                    # Remove 'export ' and parse KEY="value"
                    env_line = line[7:]  # Remove 'export '
                    if '=' in env_line:
                        key, value = env_line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip('"\'')
                        os.environ[key] = value
            
            print("✅ Loaded secrets from secure storage")
            return True
            
        except Exception as e:
            print(f"⚠️ Could not load secure secrets: {e}")
            return False
    
    return False

# Load secure secrets immediately when this module is imported
_load_secure_secrets()

# Fallback to .env only if secure loading failed
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except ImportError:
    pass

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
if os.getenv('ENVIRONMENT') == 'prod':
    ALLOWED_SLACK_USERS = [
        # "U08V5JXD84C",# son0004@kzgroup.biz
        "U08TP7RP2NM",# Estelle
        "U080EAXBDHC",# Daniela
        "U080JHRANCR" # Sam
    ]
else:
    ALLOWED_SLACK_USERS = [
        "U0904UHELTE",# son_developer
        "U090U17T94G",# son0004@kzgroup.biz
        "U090GBUM3HV",# Estelle
        "U0918U4HSD6",# Daniela
        "U090GBYU971" # Sam
    ]