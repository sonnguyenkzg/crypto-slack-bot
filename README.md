# USDT Wallet Balance Slack Bot

A Python bot that automatically monitors USDT (TRC20) wallet balances, maintains historical records, generates trend charts, and sends comprehensive reports to Slack channels. Designed for automated periodic execution to provide continuous cryptocurrency asset monitoring.

## Features

- **Multi-wallet tracking**: Monitor balances across multiple USDT TRC20 wallets
- **Historical logging**: Automatic CSV-based balance history storage
- **Visual reporting**: Dynamic trend charts with individual wallet subplots
- **Slack integration**: Automated text summaries and chart delivery
- **Timezone consistency**: All timestamps use GMT+7
- **Error handling**: Robust API, file, and communication error management
- **Automated scheduling**: Cron-ready for hands-off operation

## How It Works

The bot follows a sequential execution flow:

1. **Configuration loading**: Reads wallet addresses and Slack credentials
2. **Balance fetching**: Queries Tronscan API for current USDT TRC20 balances
3. **Data logging**: Appends timestamped balance data to CSV file
4. **Chart generation**: Creates trend visualization from historical data
5. **Slack reporting**: Delivers formatted summary and chart to designated channel

## Prerequisites

- Python 3.8 or higher
- pip package installer
- Git for repository cloning
- Slack workspace with configured bot application

### Slack App Requirements

Your Slack app needs these OAuth scopes:
- `chat:write` - Post messages to channels
- `files:write` - Upload chart images

You'll need to obtain:
- Bot User OAuth Token (starts with `xoxb-`)
- Target Slack Channel ID

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sonnguyenkzg/crypto-slack-bot.git
   cd crypto-slack-bot
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SLACK_BOT_TOKEN="xoxb-YOUR_SLACK_BOT_TOKEN_HERE"
   SLACK_CHANNEL_ID="YOUR_SLACK_CHANNEL_ID_HERE"
   ```

4. **Configure wallet addresses**
   
   Edit `bot/config.py` to add your wallet addresses:
   ```python
   WALLETS = {
       "Main Wallet": "TRON_WALLET_ADDRESS_1",
       "Trading Wallet": "TRON_WALLET_ADDRESS_2",
       # Add additional wallets as needed
   }
   ```

## Configuration Options

Key settings in `bot/config.py`:

- **WALLETS**: Dictionary mapping wallet names to TRC20 addresses
- **NUM_RECORDS_TO_PLOT**: Number of historical records to display in charts (default: 13)

## Usage

### Manual Execution

For testing and immediate execution:

```bash
source .venv/bin/activate
python main.py
```

### Automated Execution

Set up automated execution using cron:

```bash
crontab -e
```

Add this line for execution every minute:
```bash
* * * * * cd /home/azureuser/crypto-slack-bot/ && /home/azureuser/crypto-slack-bot/.venv/bin/python main.py >> /home/azureuser/crypto-slack-bot/cron.log 2>&1
```

**Note**: Adjust the path `/home/azureuser/crypto-slack-bot/` to match your installation directory.

## Output Files

The bot generates several files during operation:

- `wallet_balances.csv` - Historical balance data with GMT+7 timestamps
- `wallet_trend.png` - Generated trend chart image
- `cron.log` - Execution logs and error messages (when run via cron)

## Troubleshooting

### Slack Integration Issues

- Verify `.env` file contains correct `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID`
- Ensure Slack app has required permissions (`chat:write`, `files:write`)
- Confirm bot is invited to the target channel
- Check `cron.log` for `SlackApiError` messages

### Chart and Timestamp Issues

- Verify all timestamps in `wallet_balances.csv` use GMT+7
- If timezone inconsistencies exist, delete `wallet_balances.csv` to regenerate
- Confirm `NUM_RECORDS_TO_PLOT` setting in `bot/config.py`

### Cron Execution Issues

- Verify cron job syntax in `crontab -l`
- Check system cron logs: `/var/log/syslog` or `journalctl -xe`
- Ensure Python virtual environment path is correct
- Confirm working directory path in cron command

### General Debugging

The `cron.log` file contains detailed execution information and error messages. Always check this file first when troubleshooting issues.

## License

This project is open source. Please check the repository for license details.

## Contributing

Contributions are welcome. Please submit pull requests or issues through the GitHub repository.