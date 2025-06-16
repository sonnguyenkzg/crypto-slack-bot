# Crypto/USDT Wallet Monitor Bot

A smart Slack bot that automatically tracks USDT (cryptocurrency) wallet balances and sends daily reports to your team. Perfect for businesses managing multiple crypto wallets across different locations or purposes.

## What Does This Bot Do?

**Automatic Monitoring**: Checks your USDT wallet balances 24/7 and sends daily summary reports  
**Real-Time Commands**: Ask for balance updates anytime by mentioning the bot in Slack  
**Historical Tracking**: Keeps a record of all balance changes in a CSV file  
**Secure & Private**: Only authorized team members can use wallet commands  
**Easy Management**: Add or remove wallets directly through Slack commands  

## How It Works

### Daily Reports (Automatic)
Every day at 12:00 AM GMT+7 (midnight), the bot automatically sends a balance summary to your Slack channel:

```
💰 Daily Balance Report

⏰ Time: 2025-06-15 00:00 GMT+7

• KZP 96G1: 0.00 USDT
• KZP BLG1: 0.00 USDT  
• KZP WDB1: 0.00 USDT
• KZP TH 1: 69,466.72 USDT
• KZP TH Y 1: 25,015.48 USDT
• KZP TH BM 1: 28.59 USDT
• KZP PH 1: 0.00 USDT
• KZP PH BM 1: 0.74 USDT
• KZP KZO1: 0.00 USDT

📊 Total: 94,511.53 USDT
```

### Interactive Commands (On-Demand)
Mention the bot in Slack to get instant updates or manage wallets:

- `@bot !check` - See all current balances
- `@bot !check "Store1"` - Check specific wallet
- `@bot !list` - Show all configured wallets
- `@bot !add "Company" "WalletName" "Address"` - Add new wallet
- `@bot !remove "WalletName"` - Remove wallet
- `@bot !help` - Show all commands

## Setup Guide

### Step 1: Create Your Slack App

1. **Go to Slack API**: Visit https://api.slack.com/apps
2. **Create New App**: Click "Create New App" → "From scratch"
3. **Name Your App**: Enter "KZG_CryptoBalanceBot_PROD" and select your workspace

### Step 2: Configure App Permissions

1. **OAuth & Permissions**: In the left sidebar, click "OAuth & Permissions"
2. **Add Bot Scopes**:
   - `chat:write` (send messages)
   - `app_mentions:read` (respond when mentioned)

### Step 3: Enable Interactive Features

1. **Socket Mode**: In the left sidebar, enable "Socket Mode"
2. **Generate App Token**: Create an App-Level Token with `connections:write` scope
3. **Save the Token**: Copy and save this token (starts with `xapp-`)

### Step 4: Install to Your Workspace

1. **Install App**: Go back to "OAuth & Permissions" and click "Install to Workspace"
2. **Authorize**: Grant the requested permissions
3. **Copy Bot Token**: Save the "Bot User OAuth Token" (starts with `xoxb-`)

### Step 5: Get Your Channel ID

1. **Find Your Channel**: Right-click your target Slack channel
2. **View Details**: Select "View channel details"
3. **Copy Channel ID**: Look for the Channel ID (format: C1234567890)
4. **Add Bot**: Type `@KZG_CryptoBalanceBot_PROD` in the channel to add the bot

## Installation

### Download and Setup

```bash
# Download the project
git clone <your-repo-url>
cd usdt-wallet-bot

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Configure Your Settings

Create a `.env` file in the project folder:

```env
SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
SLACK_APP_TOKEN="xapp-your-app-token-here"  
SLACK_CHANNEL_ID="C1234567890"
```

### Start the Bot

Make the startup script executable and run it:

```bash
chmod +x start_secure.sh
./start_secure.sh
```

That's it! Your bot is now:
- Running 24/7 and responding to commands
- Sending daily reports at 12:00 AM GMT+7 (midnight)
- Keeping historical records in CSV format

## Using the Bot

### Adding Your First Wallet

In Slack, mention the bot and use the add command:

```
@bot !add "MyCompany" "MainStore" "TNZkbytSMdaRJ79CYzv8BGK6LWNmQxcuM8"
```

### Checking Balances

```
@bot !check                    # All wallets
@bot !check "MainStore"        # Specific wallet  
@bot !list                     # Show all wallets
```

### Managing Wallets

```
@bot !remove "MainStore"       # Remove a wallet
@bot !help                     # Show all commands
```

## Security Features

- **User Authorization**: Only pre-approved team members can use commands
- **Secure Token Storage**: Supports secure credential management in production
- **Read-Only Access**: Bot only reads wallet balances, cannot make transactions
- **Channel Restrictions**: Bot only works in your designated channel

## File Structure

```
usdt-wallet-bot/
├── bot/                      # Core bot modules
├── main.py                   # Daily report scheduler  
├── slack_listener.py         # Interactive command handler
├── start_secure.sh          # Safe startup script
├── .env                     # Your tokens (create this)
├── wallets.json            # Wallet storage (auto-created)
├── wallet_balances.csv     # Historical data (auto-created)
└── README.md               # This guide
```

## Monitoring and Maintenance

### Check Bot Status
```bash
ps aux | grep slack_listener  # See if bot is running
tail -f slack_listener.log    # View command logs
tail -f reports.log          # View daily report logs
```

### Restart Bot
```bash
./start_secure.sh            # Safely restart (stops old instances first)
```

### Stop Bot
```bash
pkill -f slack_listener      # Stop the bot
```

## Troubleshooting

**Bot not responding?**
- Check if it's running: `ps aux | grep slack_listener`
- Restart with: `./start_secure.sh`
- Check logs: `tail -f slack_listener.log`

**Daily reports not coming?**
- Check cron job: `crontab -l`
- Test manually: `python main.py`
- Check logs: `tail -f reports.log`

**Permission denied errors?**
- Make sure your user ID is in the authorized list
- Contact your administrator to add you

**Commands not working?**
- Always mention the bot: `@bot !command`
- Use quotes around wallet names: `!check "My Wallet"`
- Check available wallets: `@bot !list`

## What Wallets Are Supported?

This bot works with **USDT TRC20** wallets only. These are USDT tokens on the Tron blockchain. Wallet addresses start with 'T' and are 34 characters long.

Examples of compatible addresses:
- TNZkbytSMdaRJ79CYzv8BGK6LWNmQxcuM8
- TARvAP993BSFBuQhjc8oG4gviskNDRtB7Z

## Need Help?

- Use `@bot !help` in Slack for command reference
- Check the logs if something isn't working
- Make sure your wallet addresses are valid TRC20 addresses
- Verify your Slack tokens are correct in the `.env` file

## Technical Details

- **API**: Uses Tronscan API for balance checking
- **Timezone**: All timestamps in GMT+7 
- **Data**: Stores balance history in CSV format
- **Precision**: Uses Python Decimal for accurate calculations
- **Architecture**: Modular design for easy maintenance