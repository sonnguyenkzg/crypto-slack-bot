# bot/csv_logger.py
"""
Module for logging wallet balance data to a CSV file.
Ensures consistent data format and handles file operations robustly.
"""
import csv
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal

from bot.config import CSV_FILE, GMT_OFFSET


def log_to_csv(wallets: dict, balances: dict, csv_filename: str = CSV_FILE):
    """
    Logs wallet balances to a CSV file. Appends new data rows.
    Creates the file and writes headers if it doesn't exist or is empty.

    Args:
        wallets (dict): Dictionary mapping wallet names to their addresses
        balances (dict): Dictionary mapping wallet names to their current USDT balances
        csv_filename (str): CSV file path. Defaults to configured CSV_FILE
    """
    # Generate timestamp in GMT+7
    gmt_now = datetime.now(timezone(timedelta(hours=GMT_OFFSET)))
    timestamp_str = gmt_now.isoformat()

    # Define header and data rows
    header_row = ["Timestamp"] + list(wallets.keys())
    data_row = [timestamp_str] + [balances.get(name, Decimal('0.0')) for name in wallets.keys()]

    try:
        file_exists = os.path.exists(csv_filename)
        file_empty = not file_exists or os.path.getsize(csv_filename) == 0

        with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if file_empty:
                writer.writerow(header_row)
            writer.writerow(data_row)
        
        print(f"✅ Balances logged to {csv_filename}")
        
    except IOError as e:
        print(f"❌ Error writing to CSV file '{csv_filename}': {e}")
    except Exception as e:
        print(f"❌ Unexpected error logging to CSV: {e}")