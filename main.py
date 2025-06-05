from bot.balance_checker import get_trx_balance
from bot.slack_reporter import send_report_to_slack
from bot.config import WALLETS, SLACK_WEBHOOK_URL
from bot.csv_logger import log_to_csv
from bot.slack_upload import 
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


balances = {name: get_trx_balance(addr) for name, addr in WALLETS.items()}
send_report_to_slack(WALLETS, balances, SLACK_WEBHOOK_URL)


log_to_csv(WALLETS, balances)
