# bot/config.py
import os

WALLETS = {
    "KZP TH Y 1": "TSpAswScHnu6WqJDaZzjWEA4ztPSzPRtPZ",
    "KZP TH BM 1": "TS928hvaYDoGNhzYJcvyDSL2EB6XjPUyTh",
    "KZP PH 1": "THB5JtMUtvmZ94HdCqqL34SzSfJavF58Ga",
    "KZP PH BM 1": "TTRpG11vBzdir9GcD4MmkUNoubGxJUpwsf"
}


SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
