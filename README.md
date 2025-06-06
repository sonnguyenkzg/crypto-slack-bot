# 💰 USDT Wallet Balance Slack Bot 📈

This Python bot automatically fetches USDT (TRC20) wallet balances, logs them historically to a CSV file, generates a visual trend chart, and sends a comprehensive report directly to a Slack channel. It's designed to run periodically (e.g., via cron) to provide continuous monitoring of your cryptocurrency assets.

---

## ✨ Features

* **Multi-Wallet Tracking:** Monitor balances for multiple configured USDT TRC20 wallets.
* **Historical Logging:** Stores balance data in a CSV file (`wallet_balances.csv`) for historical trend analysis.
* **Dynamic Charting:** Generates clear, multi-panel trend charts (`wallet_trend.png`) visualizing each wallet's balance changes over time.
    * Plots individual wallet trends on separate subplots for clarity.
    * Displays current balance directly in each subplot's title.
    * Consistently uses GMT+7 for all timestamps.
* **Slack Integration:** Sends both a text summary and the generated chart image to a specified Slack channel.
* **Robust & Resilient:** Includes error handling for API calls, file operations, and Slack communication.
* **Automated Execution:** Easily configurable for scheduled runs using `cron`.

---

## 🚀 How It Works (High-Level Flow)

The bot operates in a sequential flow:

1.  **Configuration Loading:** Loads wallet addresses and Slack API credentials from `bot/config.py` and environment variables.
2.  **Balance Fetching:** Queries the Tronscan API for the current USDT TRC20 balance of each configured wallet.
3.  **Data Logging:** Appends the fetched balances and a GMT+7 timestamp to `wallet_balances.csv`.
4.  **Chart Generation:** Reads historical data from `wallet_balances.csv`, processes it, and generates `wallet_trend.png`.
5.  **Slack Reporting:** Sends the formatted text summary and the generated chart image to your designated Slack channel.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your Ubuntu VM (or similar Linux environment):

* **Python 3.8+** (or compatible version)
* **pip** (Python package installer)
* **git** (for cloning the repository)
* **A Slack Workspace and App:**
    * You'll need a Slack App with specific permissions.
    * Obtain a **Bot User OAuth Token** (starts with `xoxb-`).
    * Get the **Channel ID** where the bot should post.

---

## 🛠️ Setup & Installation Guide

Follow these steps to get your bot up and running:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/sonnguyenkzg/crypto-slack-bot.git](https://github.com/sonnguyenkzg/crypto-slack-bot.git)
    cd crypto-slack-bot
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
    (You'll see `(.venv)` prepended to your terminal prompt, indicating it's active.)

4.  **Install Dependencies:**
    Install all required Python libraries.
    ```bash
    pip install -r requirements.txt
    ```

### **5. Configure Environment Variables (`.env` file) & Slack App Setup:**

Your bot communicates with Slack using a Bot User OAuth Token and a Channel ID. These should be kept secure and managed as environment variables.

1.  **Create your Slack App (if not already done):**
    * Go to [api.slack.com/apps](https://api.slack.com/apps) and click "Create New App".
    * Choose "From scratch" and give it a name and select your Slack workspace.
    * In the "Features" section of your app, navigate to **"OAuth & Permissions"**.
    * **Add Bot Token Scopes:** Scroll down to "Scopes" -> "Bot Token Scopes" and click "Add an OAuth Scope". Add the following:
        * `chat:write`: Allows the bot to post messages in channels it's invited to.
        * `files:write`: Allows the bot to upload files (your trend chart).
    * Scroll back up and click "Install to Workspace" (or "Reinstall to Workspace" if you've changed scopes).

2.  **Obtain Credentials:**
    * After installing the app, you will find your **Bot User OAuth Token** (starts with `xoxb-`) at the top of the "OAuth & Permissions" page.
    * To get your **Slack Channel ID**: Open Slack in your browser, go to the channel, and the ID (e.g., `C1234567890`) will be the last part of the URL (e.g., `https://app.slack.com/client/T12345678/C1234567890`).

3.  **Create the `.env` file:**
    In the root of your project directory (`/home/azureuser/crypto-slack-bot/.env`), create a file named `.env` and add your obtained credentials:
    ```dotenv
    SLACK_BOT_TOKEN="xoxb-YOUR_SLACK_BOT_TOKEN_HERE"
    SLACK_CHANNEL_ID="YOUR_SLACK_CHANNEL_ID_HERE"
    ```
    * **Replace the placeholders** with your actual token and channel ID.

---

## ⚙️ Configuration

All core configurations for the bot are managed in `bot/config.py`.

* **`WALLETS`**: This dictionary holds the names and corresponding USDT TRC20 wallet addresses you wish to monitor.
    ```python
    # bot/config.py excerpt
    WALLETS = {
        "Wallet Name 1": "TRON_WALLET_ADDRESS_1",
        "Wallet Name 2": "TRON_WALLET_ADDRESS_2",
        # Add more wallets as needed
    }
    ```
    * **Important:** Ensure these are valid USDT TRC20 addresses on the Tron network.

* **`NUM_RECORDS_TO_PLOT`**: Defines how many of the latest historical balance records will be displayed on the trend chart.
    ```python
    # bot/config.py excerpt
    NUM_RECORDS_TO_PLOT = 13 # Adjust to your desired number of data points
    ```

* **Slack Credentials (`SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`):** While fetched from `.env`, they are imported into `main.py` via `config.py`, making `config.py` the central point for parameter access.

---

## ▶️ Running the Bot

### **1. Manually (for testing):**

You can run the bot manually to test its functionality and see immediate output.

```bash
# Make sure your virtual environment is active
source .venv/bin/activate
python main.py