#!/bin/bash
# start_bot.sh - Start USDT Wallet Bot Services

echo "🚀 Starting USDT Wallet Bot..."

# Activate virtual environment
source .venv/bin/activate

# Start interactive bot in background (24/7 commands)
echo "📡 Starting interactive command bot..."
nohup python slack_listener.py > slack_listener.log 2>&1 &
echo "✅ Interactive bot started (PID: $!)"

# Add cron job for daily reports at midnight GMT+7
echo "📅 Setting up daily reports..."
SCRIPT_DIR=$(pwd)
(crontab -l 2>/dev/null | grep -v "main.py"; echo "0 17 * * * cd $SCRIPT_DIR && $SCRIPT_DIR/.venv/bin/python main.py >> $SCRIPT_DIR/reports.log 2>&1") | crontab -

echo "✅ Setup complete!"
echo ""
echo "📊 Your bot is now running:"
echo "  🤖 Interactive commands: 24/7 (logs: slack_listener.log)"
echo "  📅 Daily reports: 00:00 GMT+7 (logs: reports.log)"
echo ""
echo "📝 Commands:"
echo "  Check status: ps aux | grep slack_listener"
echo "  View logs: tail -f slack_listener.log"
echo "  Stop bot: pkill -f slack_listener"
