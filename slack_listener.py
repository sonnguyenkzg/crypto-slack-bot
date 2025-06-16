#!/usr/bin/env python3
# slack_listener.py
"""
Slack message listener for wallet commands.
Mention-only mode - bot only responds when directly mentioned.
"""
import os
import time
import re
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from dotenv import load_dotenv

from bot.slack_commands import handle_slack_command
from bot.config import ALLOWED_SLACK_USERS

# Load environment variables
load_dotenv()

# Configuration
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')
SLACK_CHANNEL_ID = os.environ.get('SLACK_CHANNEL_ID')

# Valid commands
VALID_COMMANDS = ['add', 'remove', 'check', 'list', 'help']


class WalletCommandBot:
    def __init__(self):
        """Initialize the bot with Slack clients and authentication."""
        self.web_client = WebClient(token=SLACK_BOT_TOKEN)
        self.socket_client = SocketModeClient(
            app_token=SLACK_APP_TOKEN,
            web_client=self.web_client
        )
        
        # Get bot user ID
        try:
            auth_response = self.web_client.auth_test()
            self.bot_user_id = auth_response["user_id"]
            print(f"✅ Bot authenticated as {auth_response['user']} ({self.bot_user_id})")
        except Exception as e:
            print(f"❌ Failed to authenticate bot: {e}")
            self.bot_user_id = None
    
    def parse_mention_command(self, message: str, user_id: str) -> tuple:
        """
        Parse command from bot mention message.
        Only processes messages that mention the bot.
        
        Args:
            message: Full message text including mention
            user_id: User ID who sent the message
            
        Returns:
            tuple: (is_command, command, text)
        """
        # Ignore messages from the bot itself
        if user_id == self.bot_user_id:
            return False, None, None
        
        # Must contain bot mention
        if f'<@{self.bot_user_id}>' not in message:
            return False, None, None
        
        # Remove the mention and extract command
        clean_message = message.replace(f'<@{self.bot_user_id}>', '').strip()
        
        # Must start with !
        if not clean_message.startswith('!'):
            return False, None, None
        
        # Parse command
        parts = clean_message[1:].split(' ', 1)
        cmd = parts[0].lower()
        
        if cmd in VALID_COMMANDS:
            command = f"!{cmd}"
            text = parts[1] if len(parts) > 1 else ""
            return True, command, text.strip()
        
        return False, None, None
    
    def format_slack_text(self, text: str) -> str:
        """Convert markdown-style formatting to Slack formatting."""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # Convert **text** to *text* (bold in Slack)
            if line.startswith('**') and line.endswith('**'):
                formatted_lines.append(f"*{line[2:-2]}*")
            elif '**' in line and line.count('**') >= 2:
                formatted_line = re.sub(r'\*\*(.*?)\*\*', r'*\1*', line)
                formatted_lines.append(formatted_line)
            elif line.startswith('• '):
                formatted_lines.append(line)
            elif line.startswith('!') or line.startswith('`!'):
                formatted_lines.append(f"`{line}`" if not line.startswith('`') else line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def handle_app_mentions(self, client: SocketModeClient, req: SocketModeRequest):
        """Handle app mention events only - mention-only mode."""
        try:
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            
            # Extract event data
            event = req.payload.get("event", {})
            event_type = event.get("type")
            
            # Only process app_mention events
            if event_type != "app_mention":
                return
            
            # Get message details
            channel_id = event.get("channel")
            user_id = event.get("user")
            message_text = event.get("text", "")
            
            # Skip bot messages
            if user_id == self.bot_user_id:
                return
            
            # Only process messages from our target channel
            if channel_id != SLACK_CHANNEL_ID:
                return
            
            # Parse command from mention
            is_command, command, text = self.parse_mention_command(message_text, user_id)
            
            if not is_command:
                # Invalid mention - show help
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text="🤖 Please use a valid command after mentioning me.\n\nExample: `@bot !help`\n\nAvailable: `!help` `!check` `!list` `!add` `!remove`",
                    mrkdwn=True
                )
                return
            
            # Check permissions
            if user_id not in ALLOWED_SLACK_USERS:
                print(f"⛔ Unauthorized command attempt by user {user_id} for command '{command}'")
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text="⛔ You do not have permission to use this command. Please contact an administrator.",
                    mrkdwn=True
                )
                return
            
            print(f"📨 Processing mention command: {command} '{text}' from user {user_id}")
            
            # Process the command
            try:
                response_text = handle_slack_command(command, text, user_id, channel_id)
                
                # Format response with headers
                if command == "!list":
                    formatted_response = f"🤖 *Wallet List*\n\n{self.format_slack_text(response_text)}"
                elif command == "!help":
                    formatted_response = f"🤖 *Help - Available Commands*\n\n{self.format_slack_text(response_text)}"
                elif command == "!check":
                    formatted_response = f"🤖 *Wallet Balance Check*\n\n{self.format_slack_text(response_text)}"
                elif command == "!add":
                    formatted_response = f"🤖 *Add Wallet Result*\n\n{self.format_slack_text(response_text)}"
                elif command == "!remove":
                    formatted_response = f"🤖 *Remove Wallet Result*\n\n{self.format_slack_text(response_text)}"
                else:
                    formatted_response = f"🤖 *Response*\n\n{self.format_slack_text(response_text)}"
                
                # Send response
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text=formatted_response,
                    mrkdwn=True
                )
                
                print(f"✅ Response sent for {command}")
                
            except Exception as e:
                print(f"❌ Error processing command {command}: {e}")
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"❌ Error processing `{command}` command. Please try again.",
                    mrkdwn=True
                )
        
        except Exception as e:
            print(f"❌ Error in mention handler: {e}")
            import traceback
            traceback.print_exc()
    
    def start(self):
        """Start the bot listener in mention-only mode."""
        if not self.bot_user_id:
            print("❌ Cannot start bot - authentication failed")
            return
        
        # Register ONLY app mention handler
        self.socket_client.socket_mode_request_listeners.append(self.handle_app_mentions)
        
        print("🚀 Starting USDT Wallet Bot (Mention-Only Mode)...")
        print(f"📡 Listening for mentions in channel: {SLACK_CHANNEL_ID}")
        print("💬 Usage (MUST mention bot):")
        print("   @bot !help     - Show commands")
        print("   @bot !check    - Check balances")
        print("   @bot !list     - List wallets")
        print("   @bot !add \"company\" \"wallet\" \"address\"")
        print("   @bot !remove \"wallet_name\"")
        print()
        print(f"🔐 Authorized users: {', '.join(ALLOWED_SLACK_USERS)}")
        print("🔒 Bot will be SILENT for non-mention messages")
        print()
        print("🔄 Bot running... Press Ctrl+C to stop")
        
        try:
            self.socket_client.connect()
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"❌ Bot error: {e}")
        finally:
            self.socket_client.disconnect()


def main():
    """Main entry point."""
    # Check required environment variables
    if not SLACK_BOT_TOKEN:
        print("❌ SLACK_BOT_TOKEN not found in environment variables")
        return
    
    if not SLACK_APP_TOKEN:
        print("❌ SLACK_APP_TOKEN not found in environment variables")
        return
    
    if not SLACK_CHANNEL_ID:
        print("❌ SLACK_CHANNEL_ID not found in environment variables")
        return
    
    # Create and start bot
    bot = WalletCommandBot()
    bot.start()


if __name__ == "__main__":
    main()