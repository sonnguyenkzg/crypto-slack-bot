# bot/csv_logger.py
"""
Module for logging wallet balance data to a CSV file.
Ensures consistent data format and handles file operations robustly.
"""
import csv
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal # <-- Import Decimal for type consistency

# WALLETS is not used directly in this module, it's passed from main.py. So, no need to import it here.
# from bot.config import WALLETS # Removed as not directly used here

def log_to_csv(wallets: dict, balances: dict, csv_filename: str = "wallet_balances.csv"):
    """
    Logs wallet balances to a CSV file. Appends new data rows.
    Creates the file and writes headers if it doesn't exist or is empty.

    Args:
        wallets (dict): A dictionary mapping wallet names to their addresses (used for header order).
        balances (dict): A dictionary mapping wallet names to their current USDT balances (expected Decimal type).
        csv_filename (str): The name of the CSV file to log data to. Defaults to "wallet_balances.csv".
    """
    # Generate timestamp in GMT+7 for consistency across the project, using ISO 8601 format
    gmt7_now = datetime.now(timezone(timedelta(hours=7)))
    timestamp_str = gmt7_now.isoformat() 

    # Define the header row based on wallet names. This order must match data_row.
    header_row = ["Timestamp"] + list(wallets.keys())
    
    # Prepare the data row, ensuring consistent Decimal type for balances.
    # Uses Decimal('0.0') as default for consistency if a wallet is unexpectedly missing.
    data_row = [timestamp_str] + [balances.get(name, Decimal('0.0')) for name in wallets.keys()] # <-- Changed 0.0 to Decimal('0.0')

    try:
        file_exists = os.path.exists(csv_filename)
        # Check if file is empty by checking its size, useful if file exists but is empty
        file_empty = not file_exists or os.path.getsize(csv_filename) == 0

        # Open file in append mode, with newline='' for csv.writer, and specify UTF-8 encoding
        with open(csv_filename, 'a', newline='', encoding='utf-8') as f: # <-- Added encoding
            writer = csv.writer(f)
            if file_empty:
                writer.writerow(header_row) # Write header only if file is new or empty
            writer.writerow(data_row)
        print(f"✅ Balances logged to {csv_filename}")
    except IOError as e:
        print(f"❌ Error writing to CSV file '{csv_filename}': {e}")
        # Log specifics about the IOError (e.g., permissions, disk space)
    except Exception as e:
        print(f"❌ An unexpected error occurred while logging to CSV: {e}")