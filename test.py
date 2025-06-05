import requests

# List of wallets (name + address)
wallets = {
    "KZP TH Y 1": "TSpAswScHnu6WqJDaZzjWEA4ztPSzPRtPZ",
    "KZP TH BM 1": "TS928hvaYDoGNhzYJcvyDSL2EB6XjPUyTh",
    "KZP PH 1": "THB5JtMUtvmZ94HdCqqL34SzSfJavF58Ga",
    "KZP PH BM 1": "TTRpG11vBzdir9GcD4MmkUNoubGxJUpwsf"
}

print("📢 KZP Wallet Balances (via Tronscan):\n")

for name, address in wallets.items():
    url = f"https://apilist.tronscanapi.com/api/account?address={address}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        raw_balance = data.get("balance", 0)
        trx_balance = raw_balance / 1_000_000  # Convert from SUN to TRX
        print(f"- {name}: {trx_balance:.2f} TRX")
    except Exception as e:
        print(f"- {name}: ❌ Error fetching balance ({e})")
