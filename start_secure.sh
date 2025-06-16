#!/bin/bash
# start_secure.sh - Safe startup script that prevents multiple instances

echo "🚀 Starting USDT Wallet Bot (Safe Mode)..."

# Activate virtual environment
source .venv/bin/activate

# Kill any existing instances first
echo "🔍 Checking for existing bot instances..."
EXISTING_PIDS=$(pgrep -f "slack_listener.py")

if [ ! -z "$EXISTING_PIDS" ]; then
    echo "⚠️ Found existing instances with PIDs: $EXISTING_PIDS"
    echo "🛑 Stopping existing instances..."
    pkill -f slack_listener.py
    sleep 2
    
    # Force kill if still running
    REMAINING=$(pgrep -f "slack_listener.py")
    if [ ! -z "$REMAINING" ]; then
        echo "💀 Force killing remaining instances..."
        pkill -9 -f slack_listener.py
        sleep 1
    fi
    echo "✅ Existing instances stopped"
else
    echo "✅ No existing instances found"
fi

# Start new instance
echo "📡 Starting new bot instance..."
nohup python slack_listener.py > slack_listener.log 2>&1 &
NEW_PID=$!

echo "✅ Bot started with PID: $NEW_PID"

# Verify it's running
sleep 2
if ps -p $NEW_PID > /dev/null; then
    echo "✅ Bot is running successfully"
    echo "📊 Check status: ps aux | grep slack_listener"
    echo "📋 View logs: tail -f slack_listener.log"
else
    echo "❌ Bot failed to start - check logs"
    exit 1
fi

# Setup cron job (only if not already exists)
if ! crontab -l 2>/dev/null | grep -q "main.py"; then
    echo "📅 Setting up daily reports..."
    SCRIPT_DIR=$(pwd)
    (crontab -l 2>/dev/null; echo "0 5 * * * cd $SCRIPT_DIR && $SCRIPT_DIR/.venv/bin/python main.py >> $SCRIPT_DIR/reports.log 2>&1") | crontab -
    echo "✅ Daily reports configured"
else
    echo "✅ Daily reports already configured"
fi

echo ""
echo "🎯 Bot Status:"
echo "  🤖 Interactive bot: Running (PID: $NEW_PID)"
echo "  📅 Daily reports: 12:00 GMT+7"
echo "  📊 Monitor: ps aux | grep slack_listener"
echo "  🛑 Stop: pkill -f slack_listener"