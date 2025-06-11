# USDT Wallet Balance Slack Bot

A Python bot that automatically monitors multiple USDT TRC20 wallet balances using the Tronscan API, maintains historical records in CSV format, and delivers text reports to Slack channels. Features dynamic wallet management through Slack commands and robust error handling for reliable automated execution.

## Features

- **Multi-wallet USDT TRC20 tracking**: Monitor balances across multiple configured wallets
- **Precision decimal handling**: Uses Python's Decimal class for accurate cryptocurrency calculations
- **Historical CSV logging**: Automatic balance history with GMT+7 timestamps in ISO 8601 format
- **Dynamic wallet management**: Add/remove wallets via Slack commands in real-time
- **Slack integration**: Automated text reports and interactive bot commands via Slack SDK
- **Robust error handling**: Comprehensive exception handling for API calls, file operations, and Slack communication
- **Timezone consistency**: All timestamps standardized to GMT+7 across the entire system
- **Modular architecture**: Clean separation of concerns across dedicated modules

## How It Works

The bot operates in two modes:

### 1. Scheduled Reporting (main.py)
Executes a sequential workflow for automated reports:
1. **Balance Fetching**: Queries Tronscan API for current USDT TRC20 balances
2. **Precision Processing**: Handles all monetary calculations using Python's Decimal class
3. **Slack Reporting**: Sends formatted text summaries to designated channels (identical to !check output)

### 2. Interactive Commands (slack_listener.py)
Real-time Slack bot that responds to user commands:
- `!add "company" "wallet_name" "address"` - Add new wallets
- `!remove "wallet_name"` - Remove existing wallets
- `!check` - Check all wallet balances
- `!check "wallet_name"` - Check specific wallet balance
- `!check "wallet1" "wallet2"` - Check multiple specific wallets
- `!list` - List all configured wallets
- `!help` - Show available commands

## Prerequisites

- Python 3.8 or higher
- pip package installer
- Git for repository cloning
- Slack workspace with configured bot application

## Slack App Setup

### Step 1: Create Slack App
1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Enter App Name: `USDT Wallet Monitor`
4. Select your workspace and click **"Create App"**

### Step 2: Configure OAuth Scopes
1. Go to **"OAuth & Permissions"** in the left sidebar
2. Under **"Bot Token Scopes"**, add these scopes:
   - `chat:write` - Send messages to channels
   - `chat:write.public` - Write in public channels

### Step 3: Enable Socket Mode (for interactive commands)
1. Go to **"Socket Mode"** in the left sidebar
2. Enable Socket Mode
3. Generate an **App-Level Token** with `connections:write` scope
4. Save this token (starts with `xapp-`)

### Step 4: Install App to Workspace
1. Go back to **"OAuth & Permissions"**
2. Click **"Install to Workspace"** and authorize
3. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

### Step 5: Get Channel ID
1. In Slack, right-click your target channel → **"View channel details"**
2. Copy the **Channel ID** (format: C1234567890)
3. Add the bot to the channel by typing `@USDT Wallet Monitor`

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd crypto-slack-bot
   ```

2. **Create Python virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
SLACK_BOT_TOKEN="xoxb-YOUR_BOT_TOKEN_HERE"
SLACK_APP_TOKEN="xapp-YOUR_APP_TOKEN_HERE"
SLACK_CHANNEL_ID="C1234567890"
```

### Initial Wallet Configuration

Your bot starts with wallets defined in `wallets.json`. You can add/remove wallets dynamically using Slack commands or by editing this file directly:

```json
{
  "KZP 96G1": {
    "company": "KZP",
    "wallet": "96G1",
    "address": "TNZkbytSMdaRJ79CYzv8BGK6LWNmQxcuM8"
  }
}
```

## Usage

### Quick Start (Both Services)

**1. Create the startup script:**
```bash
nano start_bot.sh
```

**2. Copy this content into the file:**
```bash
#!/bin/bash
# start_bot.sh - Start USDT Wallet Bot Services

echo "🚀 Starting USDT Wallet Bot..."

# Activate virtual environment
source .venv/bin/activate

# Start interactive bot in background (24/7 commands)
echo "📡 Starting interactive command bot..."
nohup python slack_listener.py > slack_listener.log 2>&1 &
echo "✅ Interactive bot started (PID: $!)"

# Add cron job for daily reports at noon GMT+7
echo "📅 Setting up daily reports..."
SCRIPT_DIR=$(pwd)
(crontab -l 2>/dev/null | grep -v "main.py"; echo "0 5 * * * cd $SCRIPT_DIR && $SCRIPT_DIR/.venv/bin/python main.py >> $SCRIPT_DIR/reports.log 2>&1") | crontab -

echo "✅ Setup complete!"
echo ""
echo "📊 Your bot is now running:"
echo "  🤖 Interactive commands: 24/7 (logs: slack_listener.log)"
echo "  📅 Daily reports: 12:00 GMT+7 (logs: reports.log)"
echo ""
echo "📝 Commands:"
echo "  Check status: ps aux | grep slack_listener"
echo "  View logs: tail -f slack_listener.log"
echo "  Stop bot: pkill -f slack_listener"
```

**3. Make it executable and run:**
```bash
chmod +x start_bot.sh
./start_bot.sh
```

**That's it! Your bot is now:**
- 🤖 **Accepting commands 24/7** in Slack
- 📅 **Sending daily reports** at 12:00 PM GMT+7

### Available Commands in Slack
- `!add "KZP" "KZP WDB2" "TEhmKXCPgX64yjQ3t9skuSyUQBxwaWY4KS"` - Add new wallet
- `!remove "KZP WDB2"` - Remove wallet
- `!check` - Check all wallet balances
- `!check "KZP 96G1"` - Check specific wallet
- `!check "KZP 96G1" "KZP WDB2"` - Check multiple specific wallets
- `!list` - List all configured wallets
- `!help` - Show help message

### Management Commands
```bash
# Check if bot is running
ps aux | grep slack_listener

# View logs
tail -f slack_listener.log    # Interactive commands
tail -f reports.log          # Daily reports

# Stop bot
pkill -f slack_listener

# Restart bot
./start_bot.sh

# Test manual report
python main.py
```

## Sample Output

### Scheduled Report (main.py)
```
*Daily Balance Report*

⏰ Time: 2025-06-11 12:00 GMT+7

• KZP 96G1: 1,250.32 USDT
• KZP BLG1: 3,418.78 USDT
• KZP WDB1: 892.00 USDT

📊 Total: 5,561.10 USDT
```

### Interactive Command Response (!check)
```
⏰ Time: 2025-06-11 14:30 GMT+7

• KZP 96G1: 1,250.32 USDT
• KZP BLG1: 3,418.78 USDT
• KZP WDB1: 892.00 USDT

📊 Total: 5,561.10 USDT
```

### Help Command Response (!help)
```
🤖 Help - Available Commands

Wallet Management:
• !add "company" "wallet" "address" - Add new wallet
• !remove "wallet_name" - Remove wallet  
• !list - List all wallets
• !check - Check all wallet balances
• !check "wallet_name" - Check specific wallet balance
• !check "wallet1" "wallet2" - Check multiple specific wallets

Examples:
    !add "KZP" "KZP WDB2" "TEhmKXCPgX64yjQ3t9skuSyUQBxwaWY4KS"
    !remove "KZP WDB2"
    !list
    !check
    !check "KZP 96G1"
    !check "KZP 96G1" "KZP WDB2"

Notes:
• All arguments must be in quotes
• TRC20 addresses start with 'T' (34 characters)
• Balance reports sent via scheduled messages
```

## Project Structure

```
crypto-slack-bot/
├── bot/
│   ├── config.py              # Configuration settings and constants
│   ├── usdt_checker.py        # USDT balance fetching via Tronscan API
│   ├── csv_logger.py          # CSV logging with timestamp handling
│   ├── wallet_manager.py      # Dynamic wallet add/remove operations
│   └── slack_commands.py      # Slack command parsing and handling
├── main.py                    # Scheduled reporting script
├── slack_listener.py          # Interactive Slack bot listener
├── start_bot.sh              # Startup script (creates this)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── wallets.json              # Wallet storage (auto-managed)
├── wallet_balances.csv       # Historical data (auto-generated)
├── slack_listener.log        # Interactive bot logs (auto-generated)
├── reports.log               # Daily report logs (auto-generated)
└── README.md                 # This file
```

## Dependencies

- **requests**: HTTP API communication with Tronscan
- **slack-sdk**: Slack API integration (WebClient, SocketModeClient)
- **python-dotenv**: Environment variable management

All other modules are Python standard library.

## API Details

### Tronscan API Integration
- **Endpoint**: `https://apilist.tronscanapi.com/api/account/tokens`
- **USDT Contract**: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` (official TRC20)
- **Timeout**: 10 seconds per request
- **Error Handling**: Comprehensive exception handling for network issues

### Slack API Integration
- **Method**: Slack SDK WebClient + SocketModeClient
- **Text Messages**: `chat_postMessage` API
- **Real-time Events**: Socket Mode for interactive commands
- **Error Handling**: SlackApiError exception handling

## Output Files

### wallets.json
Dynamic wallet storage with structure:
```json
{
  "wallet_name": {
    "company": "company_code",
    "wallet": "wallet_identifier", 
    "address": "TRC20_address"
  }
}
```

### wallet_balances.csv
Historical balance data with columns:
- `Timestamp`: ISO 8601 format with GMT+7 timezone
- Individual wallet columns with precise decimal balances

## Configuration Options

Key settings in `bot/config.py`:
- **API_TIMEOUT**: Request timeout for Tronscan API (default: 10 seconds)
- **GMT_OFFSET**: Timezone offset (default: 7 for GMT+7)
- **USDT_CONTRACT**: Official USDT TRC20 contract address
- **File paths**: Configurable paths for wallets.json and CSV output

## Development Notes

- All monetary calculations use `Decimal` class for precision
- Timestamps consistently use GMT+7 timezone across all modules
- Modular design allows easy extension and maintenance
- Comprehensive error handling prevents silent failures
- Type hints improve code clarity and IDE support
- Dynamic wallet management through JSON storage

## Troubleshooting

**Bot not responding to commands?**
```bash
# Check if it's running
ps aux | grep slack_listener

# If not running, start it
./start_bot.sh
```

**Daily reports not sending?**
```bash
# Check cron job exists
crontab -l

# Test manual report
python main.py
```

**Check logs for errors:**
```bash
tail -f slack_listener.log    # Interactive bot issues
tail -f reports.log          # Daily report issues
```

**Common fixes:**
- Make sure bot is added to Slack channel
- Check .env file has correct tokens
- Verify internet connection for API calls