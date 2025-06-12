#!/bin/bash
# start_secure.sh - Load secrets and start bot

echo "🔐 Loading secrets..."
# Load secrets using sudo
eval $(sudo cat /opt/usdt-bot-secrets/config)

# Activate virtual environment
source .venv/bin/activate

# Start bot in background
echo "🤖 Starting bot..."
nohup python slack_listener.py > slack_listener.log 2>&1 &
echo "✅ Bot started with PID: $!"

# Setup cron for daily reports
SCRIPT_DIR=$(pwd)
(crontab -l 2>/dev/null | grep -v "main.py"; echo "0 5 * * * sudo -E bash -c 'source /opt/usdt-bot-secrets/config && cd $SCRIPT_DIR && $SCRIPT_DIR/.venv/bin/python main.py' >> $SCRIPT_DIR/reports.log 2>&1") | crontab -

echo "📅 Daily reports scheduled"
echo ""
echo "✅ Setup complete! Bot is running securely."
