# USDT Wallet Balance Slack Bot

A Python bot that automatically monitors multiple USDT TRC20 wallet balances using the Tronscan API and delivers reports to Slack channels. Features dynamic wallet management through Slack commands and automated daily reporting.

## Features

- **Multi-wallet USDT TRC20 tracking**: Monitor balances across multiple configured wallets
- **Automated daily reports**: Scheduled balance summaries sent to Slack at 12:00 PM GMT+7
- **Interactive Slack commands**: Real-time wallet management and balance checking
- **Dynamic wallet management**: Add/remove wallets via Slack commands
- **Historical logging**: Automatic balance history with timestamps
- **Robust error handling**: Comprehensive exception handling for reliable operation

## Quick Start

### Prerequisites
- Ubuntu 24.04 LTS server
- Python 3.11+ (usually pre-installed)
- Slack workspace with bot permissions

### 1. Installation
```bash
# Clone repository
git clone https://github.com/yourusername/crypto-slack-bot.git
cd crypto-slack-bot

# Set up Python environment
sudo apt update && sudo apt install python3.12-venv -y
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip3 install slack-sdk python-dotenv requests
```

### 2. Configuration
```bash
# Create environment file
cat > .env << 'EOF'
SLACK_BOT_TOKEN="xoxb-YOUR_BOT_TOKEN_HERE"
SLACK_APP_TOKEN="xapp-YOUR_APP_TOKEN_HERE"
SLACK_CHANNEL_ID="C1234567890"
EOF
```

### 3. Start Services
```bash
# Set up daily reports (12:00 PM GMT+7)
echo "0 5 * * * cd $(pwd) && $(pwd)/.venv/bin/python main.py >> $(pwd)/reports.log 2>&1" | crontab -

# Start interactive bot
nohup python3 slack_listener.py > slack_listener.log 2>&1 &

# Verify running
ps aux | grep slack_listener
```

### 4. Test in Slack
```
!help     # Show available commands
!check    # Check all wallet balances
!list     # List configured wallets
```

## Slack Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!check` | Check all wallet balances | `!check` |
| `!check "wallet"` | Check specific wallet | `!check "KZP 96G1"` |
| `!add "company" "wallet" "address"` | Add new wallet | `!add "KZP" "WDB2" "TEhm..."` |
| `!remove "wallet"` | Remove wallet | `!remove "KZP WDB2"` |
| `!list` | List all wallets | `!list` |
| `!help` | Show help message | `!help` |

## Management Commands

### Check Status
```bash
# Check if bot is running
ps aux | grep slack_listener

# View recent activity
tail -f slack_listener.log    # Interactive bot logs
tail -f reports.log          # Daily report logs
```

### Restart Bot
```bash
# Stop and restart
pkill -f slack_listener
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

### Update Bot
```bash
# Pull latest changes
git pull origin main

# Restart services
pkill -f slack_listener
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

## Slack App Setup

### Step 1: Create Slack App
1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Enter App Name: `USDT Wallet Monitor`
4. Select your workspace

### Step 2: Configure Permissions
1. **OAuth & Permissions** → **Bot Token Scopes**:
   - `chat:write` - Send messages
   - `chat:write.public` - Write in public channels

### Step 3: Enable Socket Mode
1. **Socket Mode** → Enable Socket Mode
2. Generate **App-Level Token** with `connections:write` scope
3. Save token (starts with `xapp-`)

### Step 4: Install to Workspace
1. **OAuth & Permissions** → **Install to Workspace**
2. Copy **Bot User OAuth Token** (starts with `xoxb-`)
3. Add bot to your channel: `@USDT Wallet Monitor`

## Sample Output

### Daily Report
```
*Daily Balance Report*

⏰ Time: 2025-06-11 12:00 GMT+7

• KZP 96G1: 1,250.32 USDT
• KZP BLG1: 3,418.78 USDT
• KZP WDB1: 892.00 USDT

📊 Total: 5,561.10 USDT
```

### Interactive Command (!check)
```
⏰ Time: 2025-06-11 14:30 GMT+7

• KZP 96G1: 1,250.32 USDT
• KZP BLG1: 3,418.78 USDT
• KZP WDB1: 892.00 USDT

📊 Total: 5,561.10 USDT
```

## Troubleshooting

### Bot Not Responding
```bash
# Check if running
ps aux | grep slack_listener

# If not running, start it
source .venv/bin/activate
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

### Daily Reports Not Sending
```bash
# Check cron job
crontab -l

# Test manual report
source .venv/bin/activate
python3 main.py
```

### Multiple Bot Instances
```bash
# Stop all instances
pkill -f slack_listener

# Start one clean instance
source .venv/bin/activate
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

## Project Structure

```
crypto-slack-bot/
├── bot/                    # Core bot modules
├── main.py                # Daily reporting script
├── slack_listener.py      # Interactive Slack bot
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── wallets.json          # Wallet storage (auto-managed)
├── *.log                 # Log files (auto-generated)
└── README.md             # This file
```

---

## For Developers

### Development Workflow
1. **Make changes** on development server
2. **Test thoroughly** before deployment
3. **Commit and push** to GitHub
4. **Deploy to production** using `git pull`

### Production Security
- Production server has **read-only** access to repository
- Cannot push changes back (security feature)
- Can only pull updates from development

### Adding New Features
```bash
# Development server
git checkout -b feature/new-command
# Make changes, test
git commit -m "Add new command"
git push origin feature/new-command

# Production server (after merge)
git pull origin main
pkill -f slack_listener
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

## Advanced Configuration

<details>
<summary>Click to expand advanced topics</summary>

### Production Security Setup

**Step 1: Secure Git Access**
```bash
# Remove push authentication
git remote set-url origin https://github.com/username/crypto-slack-bot.git
git config --unset user.name
git config --unset user.email
```

**Step 2: Set Read-Only Identity**
```bash
git config --local user.name "PRODUCTION-READ-ONLY"
git config --local user.email "production@readonly.local"
```

**Step 3: Verify Security**
```bash
git pull origin main     # ✅ Should work
git push origin main     # ❌ Should fail (security)
```

### Change Management

**Development Phase:**
- Make changes on development server
- Test all functionality thoroughly
- Use feature branches for complex changes

**Deployment Phase:**
```bash
# Production deployment checklist
cd /path/to/crypto-slack-bot
source .venv/bin/activate
pkill -f slack_listener
git pull origin main
pip3 install -r requirements.txt  # If dependencies changed
python3 main.py  # Test functionality
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
# Test in Slack
```

**Rollback Procedure:**
```bash
git log --oneline -5  # Find previous working commit
git checkout PREVIOUS_COMMIT_HASH
pkill -f slack_listener
nohup python3 slack_listener.py > slack_listener.log 2>&1 &
```

### Environment Variables

Required in `.env` file:
- `SLACK_BOT_TOKEN` - Bot User OAuth Token
- `SLACK_APP_TOKEN` - App-Level Token  
- `SLACK_CHANNEL_ID` - Target channel ID

Optional:
- `SLACK_WEBHOOK_URL` - Alternative webhook URL
- `SLACK_SIGNING_SECRET` - For webhook verification

### API Details

**Tronscan API:**
- Endpoint: `https://apilist.tronscanapi.com/api/account/tokens`
- USDT Contract: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`
- Timeout: 10 seconds per request

**Slack API:**
- Uses Slack SDK with WebClient and SocketModeClient
- Real-time events via Socket Mode
- Text messages via `chat_postMessage`

</details>

## Support

- **Issues**: Create GitHub issue for bugs or feature requests
- **Documentation**: Check this README for common solutions
- **Logs**: Monitor `slack_listener.log` and `reports.log` for debugging

## License

This project is licensed under the MIT License - see the LICENSE file for details.