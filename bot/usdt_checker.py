import requests
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from bot.config import WALLETS

USDT_CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"  # Official USDT-TRC20

def get_usdt_trc20_balance(address: str) -> float:
    """Fetch USDT TRC20 balance using Tronscan."""
    url = f"https://apilist.tronscanapi.com/api/account/tokens?address={address}"
    resp = requests.get(url)
    data = resp.json().get("data", [])
    for token in data:
        if token.get("tokenId") == USDT_CONTRACT:
            raw_balance = Decimal(token.get("balance", "0"))
            return float(raw_balance / Decimal(1_000_000))
    return 0.0

def fetch_all_usdt_balances():
    """Fetch balances for all wallets from config."""
    balances = {name: get_usdt_trc20_balance(addr) for name, addr in WALLETS.items()}
    total = sum(balances.values())

    gmt7_now = datetime.now(timezone(timedelta(hours=7)))
    time_str = gmt7_now.strftime("%Y-%m-%d %H:%M")

    lines = [f"*💵 USDT TRC20 Wallet Balances*", f"_As of {time_str} GMT+7_", ""]
    for name, value in balances.items():
        lines.append(f"- `{name}`: *{value:,.2f} USDT*")
    lines.append("")
    lines.append(f"➕ *Total*: *{total:,.2f} USDT*")

    return "\n".join(lines), balances
