
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient

load_dotenv()

bot_token = os.getenv("SLACK_BOT_TOKEN")
app_token = os.getenv("SLACK_APP_TOKEN")

print(f"Bot token: {bot_token[:10] if bot_token else 'None'}...")
print(f"App token: {app_token[:10] if app_token else 'None'}...")

# Test basic bot connection
try:
    client = WebClient(token=bot_token)
    auth_test = client.auth_test()
    print(f"✅ Bot authentication successful: {auth_test['user']}")
except Exception as e:
    print(f"❌ Bot authentication failed: {e}")

# Test Socket Mode connection
try:
    socket_client = SocketModeClient(app_token=app_token, web_client=client)
    print("✅ Socket Mode client created successfully")
except Exception as e:
    print(f"❌ Socket Mode client failed: {e}")