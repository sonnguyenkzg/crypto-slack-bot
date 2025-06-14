#!/bin/bash
# start_secure.sh - Load secrets and start bot

echo "🔐 Loading secrets..."

# Get absolute paths (dynamic, works for any user)
SCRIPT_DIR="$(pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

# Start bot in background with environment loaded
echo "🤖 Starting bot..."
nohup sudo bash -c "source /opt/usdt-bot-secrets/config && cd $SCRIPT_DIR && $VENV_PYTHON slack_listener.py" > slack_listener.log 2>&1 &
BOT_PID=$!
echo "✅ Bot started with PID: $BOT_PID"

# Setup cron for daily reports  
(crontab -l 2>/dev/null | grep -v "main.py"; echo "0 17 * * * sudo bash -c 'source /opt/usdt-bot-secrets/config && cd $SCRIPT_DIR && $VENV_PYTHON main.py' >> $SCRIPT_DIR/reports.log 2>&1") | crontab -

echo "📅 Daily reports scheduled (12:00 AM GMT+7)"
echo ""
echo "✅ Setup complete! Bot is running securely."
echo ""
echo "📝 Management commands:"
echo "  Check status: ps aux | grep slack_listener"
echo "  View logs: tail -f slack_listener.log"
echo "  Stop bot: sudo pkill -f slack_listener"