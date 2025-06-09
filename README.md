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
3. **CSV Logging**: Appends timestamped balance data with GMT+7 timezone consistency
4. **Slack Reporting**: Sends formatted text summaries to designated channels

### 2. Interactive Commands (slack_listener.py)
Real-time Slack bot that responds to user commands:
- `!add "company" "wallet" "address"` - Add new wallets
- `!remove "wallet_name"` - Remove existing wallets
- `!check` - Check current balances on demand
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
   - `files:write` - Upload files (if needed in future)

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

### Scheduled Reports (Automated)

Run the main bot for automated balance reporting:

```bash
# Test manually
python main.py
```

**For automated execution with cron (daily at midnight GMT+7):**
```bash
# Edit crontab
crontab -e

# Add line for daily execution at midnight GMT+7 (17:00 UTC if server is UTC)
0 17 * * * cd /path/to/crypto-slack-bot && /path/to/.venv/bin/python main.py >> cron.log 2>&1
```

### Interactive Commands (Real-time)

Start the interactive Slack bot:

```bash
python slack_listener.py
```

**Available Commands in Slack:**
- `!add "KZP" "WDB2" "TEhmKXCPgX64yjQ3t9skuSyUQBxwaWY4KS"` - Add new wallet
- `!remove "KZP WDB2"` - Remove wallet
- `!check` - Check all wallet balances
- `!check "KZP 96G1"` - Check specific wallet
- `!list` - List all configured wallets
- `!help` - Show help message

## Sample Output

### Scheduled Report (main.py)
```
💵 USDT TRC20 Wallet Balances 💵
As of 2025-06-09 00:00 GMT+7

• KZP 96G1: 1,250.32 USDT
• KZP BLG1: 3,418.78 USDT
• KZP WDB1: 892.00 USDT

➕ Total: 5,561.10 USDT
```

### Interactive Command Response (!check)
```
🤖 Wallet Balance Check

💰 Balance Report (3 wallets)

• KZP 96G1: 1,250.32 USDT
• KZP BLG1: 3,418.78 USDT
• KZP WDB1: 892.00 USDT

📊 Total: 5,561.10 USDT
⏰ Checked: 2025-06-09 14:30 GMT+7
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
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── wallets.json              # Wallet storage (auto-managed)
├── wallet_balances.csv       # Historical data (auto-generated)
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

**Common Issues:**
1. **"Bot not responding"** - Check SLACK_APP_TOKEN is set for interactive commands
2. **"Permission denied"** - Ensure bot has `chat:write` scope and is added to channel
3. **"API timeout"** - Increase API_TIMEOUT in config.py if network is slow
4. **"No wallets configured"** - Check wallets.json exists and has valid format

**Logs:**
- Console output shows detailed operation status
- Use `python slack_listener.py` to see real-time command processing
- Check cron.log for scheduled execution history