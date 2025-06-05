import requests

def get_trx_balance(address):
    url = f"https://apilist.tronscanapi.com/api/account?address={address}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data.get("balance", 0) / 1_000_000
    except Exception as e:
        return None
