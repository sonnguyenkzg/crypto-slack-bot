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

- **Ubuntu 24.04 LTS** (or similar Linux distribution)
- **Python 3.11+** (usually pre-installed)
- **Git** (usually pre-installed)
- **Internet connection** for API calls
- **Slack workspace** with bot permissions

## Complete Installation Guide (Ubuntu 24.04)

### Step 1: Server Preparation

```bash
# Check your system (no installation needed)
python3 --version          # Should show Python 3.11+
git --version              # Should show git 2.43+
lsb_release -a            # Confirm Ubuntu 24.04
timedatectl               # Check timezone (important for cron scheduling)
```

### Step 2: Install Required System Packages

```bash
# Update package list
sudo apt update

# Install Python virtual environment support
sudo apt install python3.12-venv -y

# Verify installation
python3 -m venv --help    # Should show venv help
```

### Step 3: Clone and Set Up Project

```bash
# Clone your repository (replace with your actual repo URL)
git clone https://github.com/yourusername/crypto-slack-bot.git
cd crypto-slack-bot

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Verify virtual environment is active
echo "Virtual env: $VIRTUAL_ENV"
which pip3
pip3 --version

# Install required Python packages
pip3 install slack-sdk python-dotenv requests

# Verify installations
pip3 list | grep -E "(slack|dotenv|requests)"
python3 -c "
import requests, slack_sdk
from dotenv import load_dotenv
print('✅ All packages imported successfully!')
"
```

### Step 4: Configure Environment Variables

Create your `.env` file with Slack credentials:

```bash
# Create .env file (replace with your actual tokens)
cat > .env << 'EOF'
SLACK_BOT_TOKEN="xoxb-YOUR_BOT_TOKEN_HERE"
SLACK_APP_TOKEN="xapp-YOUR_APP_TOKEN_HERE" 
SLACK_CHANNEL_ID="C1234567890"
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WEBHOOK_HERE"
SLACK_SIGNING_SECRET="your_signing_secret_here"
EOF

# Verify .env file
cat .env
```

### Step 5: Set Up Automated Services

```bash
# Set up cron job for daily reports at 12:00 PM GMT+7 (05:00 UTC)
echo "0 5 * * * cd /home/ubuntu/crypto-slack-bot && /home/ubuntu/crypto-slack-bot/.venv/bin/python main.py >> /home/ubuntu/crypto-slack-bot/reports.log 2>&1" | crontab -

# Verify cron job
crontab -l

# Start interactive Slack bot
nohup python3 slack_listener.py > slack_listener.log 2>&1 &

# Verify bot is running
ps aux | grep slack_listener
```

### Step 6: Test Your Installation

```bash
# Test daily report manually
python3 main.py

# Check if bot responds to Slack commands
# Go to your Slack channel and send: !check
```

## Bot Management Commands

### Check Bot Status

```bash
# Check if interactive bot is running
ps aux | grep slack_listener

# Count how many instances are running
ps aux | grep slack_listener | grep -v grep | wc -l

# Check cron job status
crontab -l

# Check recent activity
tail -f slack_listener.log    # Interactive bot logs
tail -f reports.log          # Daily report logs
```

### Start/Stop/Restart Bot

```bash
# Stop all bot instances (clean shutdown)
pkill -f slack_listener

# Verify all instances stopped
ps aux | grep slack_listener

# Start ONE clean instance
nohup python3 slack_listener.py > slack_listener.log 2>&1 &

# Verify exactly ONE instance is running
ps aux | grep slack_listener | grep -v grep
```

### Advanced Bot Management

```bash
# Kill specific bot instance by PID
kill 5619  # Replace 5619 with actual PID

# Force kill if normal kill doesn't work
kill -9 5619

# Start bot with custom log file
nohup python3 slack_listener.py > custom_bot.log 2>&1 &

# Monitor bot in real-time
tail -f slack_listener.log

# Check bot memory usage
ps aux | grep slack_listener | awk '{print $6}'  # Memory in KB

# Restart bot (complete cycle)
pkill -f slack_listener && sleep 2 && nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

### Troubleshooting Commands

```bash
# Check if bot can connect to Slack
python3 -c "
from slack_sdk import WebClient
from dotenv import load_dotenv
import os
load_dotenv()
client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
response = client.auth_test()
print('✅ Slack connection OK:', response['user'])
"

# Test wallet API connection
python3 -c "
import requests
response = requests.get('https://apilist.tronscanapi.com/api/account/tokens?address=TNZkbytSMdaRJ79CYzv8BGK6LWNmQxcuM8', timeout=10)
print('✅ Tronscan API OK:', response.status_code)
"

# Check virtual environment
echo "Python path: $(which python3)"
echo "Pip path: $(which pip3)"
echo "Virtual env: $VIRTUAL_ENV"

# Verify package versions match requirements
pip3 list | grep -E "(slack|dotenv|requests)"
```

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

## Available Commands in Slack

- `!add "KZP" "KZP WDB2" "TEhmKXCPgX64yjQ3t9skuSyUQBxwaWY4KS"` - Add new wallet
- `!remove "KZP WDB2"` - Remove wallet
- `!check` - Check all wallet balances
- `!check "KZP 96G1"` - Check specific wallet
- `!check "KZP 96G1" "KZP WDB2"` - Check multiple specific wallets
- `!list` - List all configured wallets
- `!help` - Show help message

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

## Server Migration Guide

### From Development to Production Server

**1. Stop Services on Old Server:**
```bash
# On OLD server
pkill -f slack_listener
crontab -r  # Remove cron jobs
```

**2. Set Up New Server:**
```bash
# On NEW server - follow complete installation guide above
git clone https://github.com/yourusername/crypto-slack-bot.git
cd crypto-slack-bot
# ... complete steps 1-6 above
```

**3. Verify Migration:**
```bash
# Check only NEW server responds
# Send !check in Slack - should get only one response
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

## Common Issues & Solutions

### Bot Not Responding to Commands

**Check bot status:**
```bash
ps aux | grep slack_listener
```

**If not running:**
```bash
cd /path/to/crypto-slack-bot
source .venv/bin/activate
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

**If multiple instances running:**
```bash
pkill -f slack_listener
# Wait 2 seconds
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

### Daily Reports Not Sending

**Check cron job:**
```bash
crontab -l
```

**If missing, add it:**
```bash
echo "0 5 * * * cd /home/ubuntu/crypto-slack-bot && /home/ubuntu/crypto-slack-bot/.venv/bin/python main.py >> /home/ubuntu/crypto-slack-bot/reports.log 2>&1" | crontab -
```

**Test manually:**
```bash
cd /path/to/crypto-slack-bot
source .venv/bin/activate
python3 main.py
```

### Environment Issues

**Virtual environment not working:**
```bash
python3 -m venv .venv --clear  # Recreate venv
source .venv/bin/activate
pip3 install slack-sdk python-dotenv requests
```

**Package import errors:**
```bash
source .venv/bin/activate  # Always activate first
pip3 install --upgrade slack-sdk python-dotenv requests
```

### Network/API Issues

**Check internet connectivity:**
```bash
curl -I https://api.slack.com
curl -I https://apilist.tronscanapi.com
```

**Test API endpoints:**
```bash
python3 -c "
import requests
print('Tronscan:', requests.get('https://apilist.tronscanapi.com/api/account/tokens?address=TNZkbytSMdaRJ79CYzv8BGK6LWNmQxcuM8').status_code)
"
```

## Development Notes

- All monetary calculations use `Decimal` class for precision
- Timestamps consistently use GMT+7 timezone across all modules
- Modular design allows easy extension and maintenance
- Comprehensive error handling prevents silent failures
- Type hints improve code clarity and IDE support
- Dynamic wallet management through JSON storage
- Always use virtual environment to avoid system package conflicts
- Monitor logs regularly to catch issues early

## Performance Monitoring

```bash
# Check bot memory usage
ps aux | grep slack_listener | awk '{print $6 " KB"}'

# Check log file sizes
ls -lh *.log

# Monitor real-time activity
tail -f slack_listener.log

# Check cron execution
grep "main.py" /var/log/syslog | tail -5

# System resource usage
df -h  # Disk usage
free -h  # Memory usage
```

## Security Best Practices

- Keep `.env` file secure (never commit to git)
- Use `.gitignore` to exclude sensitive files
- Regularly update dependencies: `pip3 install --upgrade -r requirements.txt`
- Monitor logs for suspicious activity
- Use specific Slack permissions (minimal required scopes)
- Consider using SSH key authentication for git repositories