# bot/slack_commands.py
"""
Slack command handlers for wallet management.
Handles parsing and validation of slash commands.
"""
import re
from typing import Tuple
from datetime import datetime, timezone, timedelta
from decimal import Decimal

from bot.config import GMT_OFFSET
from bot.wallet_manager import add_wallet, remove_wallet, list_wallets, load_wallets, validate_trc20_address
from bot.usdt_checker import get_usdt_trc20_balance


def parse_quoted_arguments(text: str) -> Tuple[bool, list]:
    """
    Parse text with quoted arguments.
    Expects exactly 3 quoted strings: "company" "wallet" "address"
    
    Args:
        text: Command text from Slack
        
    Returns:
        Tuple[bool, list]: (success, [company, wallet, address] or error_message)
    """
    if not text or not text.strip():
        return False, "❌ Missing arguments"
    
    # Find all quoted strings
    quoted_pattern = r'"([^"]*)"'
    matches = re.findall(quoted_pattern, text.strip())
    
    if len(matches) != 3:
        return False, f"❌ Expected 3 quoted arguments, found {len(matches)}"
    
    company, wallet, address = matches
    
    # Validate none are empty
    if not company.strip():
        return False, "❌ Company cannot be empty"
    if not wallet.strip():
        return False, "❌ Wallet name cannot be empty"  
    if not address.strip():
        return False, "❌ Address cannot be empty"
    
    return True, [company.strip(), wallet.strip(), address.strip()]


def handle_add_command(text: str) -> str:
    """
    Handle !add command with enforced quotes.
    
    Args:
        text: Command arguments from Slack
        
    Returns:
        str: Response message
    """
    # Parse arguments
    success, result = parse_quoted_arguments(text)
    if not success:
        error_msg = result
        return f"""{error_msg}

**Usage:** `!add "company" "wallet_name" "address"`
**Example:** `!add "KZP" "KZP WDB2" "TEhmKXCPgX64yjQ3t9skuSyUQBxwaWY4KS"`"""
    
    company, wallet, address = result
    
    # Attempt to add wallet
    success, message = add_wallet(company, wallet, address)
    
    if success:
        return f"""✅ **Wallet Added Successfully**

📋 **Details:**
• Company: {company}
• Wallet: {wallet}
• Address: {address[:10]}...{address[-6:]}

Use `!check` to see current balance."""
    else:
        return message


def handle_remove_command(text: str) -> str:
    """
    Handle !remove command.
    
    Args:
        text: Command arguments from Slack
        
    Returns:
        str: Response message
    """
    if not text or not text.strip():
        return """❌ Missing wallet name

**Usage:** `!remove "wallet_name"`
**Example:** `!remove "KZP WDB2"`"""
    
    # Parse single quoted argument for wallet name
    quoted_pattern = r'"([^"]*)"'
    matches = re.findall(quoted_pattern, text.strip())
    
    if len(matches) != 1:
        return f"""❌ Expected 1 quoted argument, found {len(matches)}

**Usage:** `!remove "wallet_name"`
**Example:** `!remove "KZP WDB2"`"""
    
    wallet_name = matches[0].strip()
    if not wallet_name:
        return "❌ Wallet name cannot be empty"
    
    # Attempt to remove wallet
    success, message = remove_wallet(wallet_name)
    return message


def handle_check_command(text: str) -> str:
    """
    Handle !check command.
    Accepts wallet names OR addresses for maximum user convenience.
    
    Args:
        text: Command arguments from Slack (optional wallet names/addresses)
        
    Returns:
        str: Response message
    """
    # Load all wallets
    wallet_data = load_wallets()
    if not wallet_data:
        return "❌ No wallets configured"
    
    # Parse inputs from text (if any)
    if not text or not text.strip():
        # Check all wallets
        wallets_to_check = {name: info['address'] for name, info in wallet_data.items()}
    else:
        # Parse quoted inputs (names or addresses)
        quoted_pattern = r'"([^"]*)"'
        inputs = re.findall(quoted_pattern, text.strip())
        
        if not inputs:
            return """❌ Invalid format. Use quotes around wallet names or addresses.

**Usage:**
• `!check` - Check all wallets
• `!check "wallet_name"` - Check by wallet name
• `!check "TRC20_address"` - Check by address
• `!check "wallet1" "TRC20_address"` - Mix names and addresses

**Examples:**
• `!check "KZP 96G1"`
• `!check "TNZkbytSMdaRJ79CYzv8BGK6LWNmQxcuM8"`
• `!check "KZP 96G1" "TARvAP993BSFBuQhjc8oG4gviskNDRtB7Z"`"""
        
        # Resolve inputs to {display_name: address}
        wallets_to_check = {}
        not_found = []
        
        for input_str in inputs:
            input_str = input_str.strip()
            
            # Check if input is a TRC20 address
            if validate_trc20_address(input_str):
                # It's an address - find the wallet name or use address as display
                found_wallet = False
                for wallet_name, wallet_info in wallet_data.items():
                    if wallet_info['address'] == input_str:
                        wallets_to_check[wallet_name] = input_str
                        found_wallet = True
                        break
                
                if not found_wallet:
                    # Address not in our monitored list - still check it
                    display_name = f"External: {input_str[:10]}...{input_str[-6:]}"
                    wallets_to_check[display_name] = input_str
            
            else:
                # It's a wallet name - find the address
                if input_str in wallet_data:
                    wallets_to_check[input_str] = wallet_data[input_str]['address']
                else:
                    not_found.append(input_str)
        
        # Report any wallet names not found
        if not_found:
            return f"""❌ Wallet name(s) not found: {', '.join(not_found)}

**Available wallet names:**
{', '.join(list(wallet_data.keys())[:5])}{'...' if len(wallet_data) > 5 else ''}

Use `!list` to see all wallets or provide TRC20 addresses directly."""
    
    # Fetch balances
    results = []
    total_balance = Decimal('0')
    successful_checks = 0
    
    for display_name, address in wallets_to_check.items():
        try:
            balance = get_usdt_trc20_balance(address)
            if balance is not None:
                results.append(f"• `{display_name}`: **{balance:,.2f} USDT**")
                total_balance += balance
                successful_checks += 1
            else:
                results.append(f"• `{display_name}`: ❌ Unable to fetch balance")
        except Exception as e:
            results.append(f"• `{display_name}`: ❌ Error: {str(e)[:50]}...")
    
    # Handle no successful checks
    if successful_checks == 0:
        return "❌ Unable to fetch any wallet balances. Please check your network connection."
    
    # Build response message
    gmt_now = datetime.now(timezone(timedelta(hours=GMT_OFFSET)))
    time_str = gmt_now.strftime("%Y-%m-%d %H:%M")
    
    if len(wallets_to_check) == 1:
        # Single wallet response
        time_line = f"⏰ **Time:** {time_str} GMT+{GMT_OFFSET}"
        wallet_list = "\n".join(results)
        message = f"{time_line}\n\n{wallet_list}"
    else:
        # Multiple wallets response
        time_line = f"⏰ **Time:** {time_str} GMT+{GMT_OFFSET}"
        footer = f"\n\n📊 **Total:** {total_balance:,.2f} USDT"
        
        if successful_checks < len(wallets_to_check):
            footer += f"\n⚠️ **Note:** {len(wallets_to_check) - successful_checks} wallet(s) failed to fetch"
        
        wallet_list = "\n".join(results)
        message = f"{time_line}\n\n{wallet_list}{footer}"
    
    return message


def handle_list_command() -> str:
    """
    Handle !list command.
    
    Returns:
        str: Response message
    """
    success, message = list_wallets()
    return message


def handle_help_command() -> str:
    """
    Handle !help command.
    
    Returns:
        str: Help message
    """
    return """**Wallet Management:**
• `!add "company" "wallet" "address"` - Add new wallet
• `!remove "wallet_name"` - Remove wallet  
• `!list` - List all wallets
• `!check` - Check all wallet balances
• `!check "wallet_name"` - Check specific wallet balance
• `!check "wallet1" "wallet2"` - Check multiple specific wallets

**Examples:**
    !add "KZP" "WDB2" "TEhmKXCPgX64yjQ3t9skuSyUQBxwaWY4KS"
    !remove "KZP WDB2"
    !list
    !check
    !check "KZP 96G1"
    !check "KZP 96G1" "KZP WDB2"

**Notes:**
• All arguments must be in quotes
• TRC20 addresses start with 'T' (34 characters)
• Balance reports sent via scheduled messages"""


def handle_slack_command(command: str, text: str, user_id: str, channel_id: str) -> str:
    """
    Main command router for Slack commands.
    
    Args:
        command: Slash command (e.g., "!add")
        text: Command arguments
        user_id: Slack user ID
        channel_id: Slack channel ID
        
    Returns:
        str: Response message
    """
    # Log command for debugging
    print(f"Command: {command}, Text: '{text}', User: {user_id}")
    
    # Route to appropriate handler
    if command == "!add":
        return handle_add_command(text)
    elif command == "!remove":
        return handle_remove_command(text)
    elif command == "!check":
        return handle_check_command(text)
    elif command == "!list":
        return handle_list_command()
    elif command == "!help":
        return handle_help_command()
    else:
        return f"""❌ Unknown command: {command}

Use `!help` for available commands."""