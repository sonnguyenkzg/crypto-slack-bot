import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import csv

def log_to_csv(wallets, balances, filepath=None):
    if not filepath:
        filepath = str(Path(__file__).resolve().parent.parent / "wallet_history.csv")

    gmt7_now = datetime.now(timezone(timedelta(hours=7)))
    timestamp = gmt7_now.strftime("%Y-%m-%d %H:%M:%S")

    row = {"Time": timestamp}
    for name in wallets:
        bal = balances.get(name)
        row[name] = round(bal, 2) if bal is not None else "ERR"

    fieldnames = ["Time"] + list(wallets.keys())
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
