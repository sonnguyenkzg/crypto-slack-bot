import requests

from datetime import datetime, timezone, timedelta

def send_report_to_slack(wallets, balances, webhook_url):
    gmt7_now = datetime.now(timezone(timedelta(hours=7)))
    timestamp = gmt7_now.strftime("%Y-%m-%d %H:%M GMT+7")

    lines = [f"📢 *KZP Wallet Balances (TRX)*\n_As of {timestamp}_\n"]
    for name in wallets:
        bal = balances.get(name)
        if bal is None:
            lines.append(f"- `{name}`: ❌ Error")
        else:
            lines.append(f"- `{name}`: *{bal:.2f} TRX*")

    message = {"text": "\n".join(lines)}
    response = requests.post(webhook_url, json=message)

    if response.status_code == 200:
        print("✅ Sent to Slack!")
    else:
        print(f"❌ Slack error: {response.status_code} - {response.text}")

