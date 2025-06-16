#!/usr/bin/env python3
# slack_listener.py
"""
Slack message listener for wallet commands.
Listens for messages in the crypto-wallet-report channel and responds to commands.
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
from bot.config import ALLOWED_SLACK_USERS # Import the allowed users list

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
    
    def is_command_message(self, message: str, user_id: str) -> tuple:
        """
        Check if message is a valid command for the bot.
        Only accepts !command format.
        
        Args:
            message: Message text
            user_id: User ID who sent the message
            
        Returns:
            tuple: (is_command, command, text)
        """
        # Ignore messages from the bot itself
        if user_id == self.bot_user_id:
            return False, None, None
        
        # Check for direct !command format
        if message.strip().startswith('!'):
            parts = message.strip()[1:].split(' ', 1)
            cmd = parts[0].lower()
            if cmd in VALID_COMMANDS:
                command = f"!{cmd}"
                text = parts[1] if len(parts) > 1 else ""
                return True, command, text.strip()
        
        # Check for bot mentions with !command
        if f'<@{self.bot_user_id}>' in message:
            # Remove the mention and check for !command
            clean_message = message.replace(f'<@{self.bot_user_id}>', '').strip()
            if clean_message.startswith('!'):
                parts = clean_message[1:].split(' ', 1)
                cmd = parts[0].lower()
                if cmd in VALID_COMMANDS:
                    command = f"!{cmd}"
                    text = parts[1] if len(parts) > 1 else ""
                    return True, command, text.strip()
        
        return False, None, None
    
    def format_slack_text(self, text: str) -> str:
        """
        Convert markdown-style formatting to Slack formatting.
        
        Args:
            text: Text with markdown formatting
            
        Returns:
            str: Text with Slack formatting
        """
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
    
    def handle_message_events(self, client: SocketModeClient, req: SocketModeRequest):
        """Handle incoming message events from Slack."""
        try:
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            
            # Extract event data
            event = req.payload.get("event", {})
            event_type = event.get("type")
            
            # DEBUG: Print what we're receiving
            print(f"🔍 DEBUG: Received event type: {event_type}")
            print(f"🔍 DEBUG: Full event data: {event}")
            
            # Handle both message and app_mention events
            if event_type not in ["message", "app_mention"]:
                print(f"🔍 DEBUG: Ignoring event type: {event_type}")
                return
            
            # Get message details
            channel_id = event.get("channel")
            user_id = event.get("user")
            message_text = event.get("text", "")
            subtype = event.get("subtype")
            
            print(f"🔍 DEBUG: Channel: {channel_id}, User: {user_id}, Text: '{message_text}'")
            print(f"🔍 DEBUG: Target channel: {SLACK_CHANNEL_ID}")
            print(f"🔍 DEBUG: Bot user ID: {self.bot_user_id}")
            
            # Skip bot messages
            if subtype == "bot_message" or user_id == self.bot_user_id:
                print(f"🔍 DEBUG: Skipping bot message")
                return
            
            # Only process messages from our target channel
            if channel_id != SLACK_CHANNEL_ID:
                print(f"🔍 DEBUG: Wrong channel - ignoring")
                return
            
            # Check if this is a command
            is_command, command, text = self.is_command_message(message_text, user_id)
            print(f"🔍 DEBUG: Command check result - is_command: {is_command}, command: {command}, text: '{text}'")
            
            if not is_command:
                # For app_mention events, if no valid command found, show help
                if event_type == "app_mention":
                    print(f"🔍 DEBUG: No valid command in app_mention - sending help")
                    self.web_client.chat_postMessage(
                        channel=channel_id,
                        text="🤖 Hi! Please use a valid command after mentioning me.\n\nUse `@bot !help` to see available commands.",
                        mrkdwn=True
                    )
                    return
                
                # For regular messages (if channels:history is available), show invalid command message
                if event_type == "message":
                    print(f"🔍 DEBUG: Invalid command in regular message")
                    self.web_client.chat_postMessage(
                        channel=channel_id,
                        text="❌ Invalid command. Use `!help` to see available commands.\n\nValid commands: `!add` `!remove` `!check` `!list` `!help`",
                        mrkdwn=True
                    )
                    print(f"⚠️ Invalid command from user: '{message_text}'")
                    return

            # --- Permission Check ---
            print(f"🔍 DEBUG: Checking permissions for user {user_id}")
            print(f"🔍 DEBUG: Allowed users: {ALLOWED_SLACK_USERS}")
            if user_id not in ALLOWED_SLACK_USERS:
                print(f"⛔ Unauthorized command attempt by user {user_id} for command '{command}'")
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text="⛔ You do not have the required permissions to use this command. Please contact an administrator.",
                    mrkdwn=True
                )
                return # Stop processing if user is not authorized
            # --- End Permission Check ---
            
            print(f"📨 Processing {event_type} command: {command} '{text}' from authorized user {user_id}")
            
            # Process the command
            try:
                response_text = handle_slack_command(command, text, user_id, channel_id)
                
                # Format response with proper headers
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
                    formatted_response = f"🤖 *CryptoBalanceBot Response*\n\n{self.format_slack_text(response_text)}"
                
                # Send response
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text=formatted_response,
                    mrkdwn=True
                )
                
                print(f"✅ Response sent for {command}")
                
            except Exception as e:
                print(f"❌ Error processing command {command}: {e}")
                
                # Send error message
                self.web_client.chat_postMessage(
                    channel=channel_id,
                    text=f"❌ Sorry, there was an error processing your `{command}` command. Please try again.",
                    mrkdwn=True
                )
        
        except Exception as e:
            print(f"❌ Error in message handler: {e}")
            import traceback
            traceback.print_exc()
            
    def start(self):
        """Start the bot listener."""
        if not self.bot_user_id:
            print("❌ Cannot start bot - authentication failed")
            return
        
        # Register event handler
        self.socket_client.socket_mode_request_listeners.append(self.handle_message_events)
        
        print("🚀 Starting USDT Wallet Command Bot...")
        print(f"📡 Listening for commands in channel: {SLACK_CHANNEL_ID}")
        print("💬 Commands (MUST start with !):")
        print("   !add \"company\" \"wallet\" \"address\"")
        print("   !remove \"wallet_name\"")
        print("   !check [wallets]")
        print("   !list")
        print("   !help")
        print("   @CryptoBalanceBot !command (mentions also work)")
        
        # Add a note about authorized users
        print(f"🔐 Only authorized users ({', '.join(ALLOWED_SLACK_USERS)}) can use management commands.")
        print()
        print("🔄 Bot is running... Press Ctrl+C to stop")
        
        try:
            # Start the socket connection
            self.socket_client.connect()
            
            # Keep the connection alive
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
        print("ℹ️  You need to enable Socket Mode and get an App Token from Slack")
        return
    
    if not SLACK_CHANNEL_ID:
        print("❌ SLACK_CHANNEL_ID not found in environment variables")
        return
    
    # Create and start bot
    bot = WalletCommandBot()
    bot.start()


if __name__ == "__main__":
    main()