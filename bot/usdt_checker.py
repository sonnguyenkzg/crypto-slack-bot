# bot/usdt_checker.py
"""
Provides functions to fetch USDT TRC20 wallet balances from the Tronscan API.
Handles API communication, data parsing, and prepares a human-readable summary.
"""
import requests
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from bot.config import WALLETS # Assuming WALLETS is always imported from config

# Official USDT TRC20 smart contract address on the Tron blockchain
# This is the Base58Check format commonly returned by Tronscan API for tokenId
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
# For reference, the address "TXLAQ63Xg1NazKPsWhHZvw7CSEMLEmqcdj" is also valid Base58,
# but the API often returns the "TR7N..." form for the tokenId.

def get_usdt_trc20_balance(address: str) -> Decimal: # <-- Change return type to Decimal for precision
    """
    Fetches the USDT TRC20 balance for a given Tron address using the Tronscan API.
    Handles network errors and unexpected API responses.

    Args:
        address (str): The Tron wallet address to query.

    Returns:
        Decimal: The USDT balance as a Decimal object, or Decimal('0.0') on error or if
                 USDT token is not found for the address.
    """
    url = f"https://apilist.tronscanapi.com/api/account/tokens?address={address}"
    
    try:
        # Add a timeout to prevent hanging indefinitely
        # Raise HTTPError for bad responses (4xx or 5xx)
        resp = requests.get(url, timeout=10) 
        resp.raise_for_status() 

        data = resp.json().get("data", []) # Default to empty list if 'data' key is missing

        if not data:
            print(f"Warning: No token data found for address {address} from Tronscan API.")
            return Decimal('0.0')

        for token in data:
            # Check if the token ID matches the USDT contract
            if token.get("tokenId") == USDT_CONTRACT:
                # Get raw balance string, default to "0" if missing
                raw_balance_str = token.get("balance", "0")
                # Convert raw balance to Decimal. Handle potential non-numeric strings safely.
                try:
                    raw_balance = Decimal(raw_balance_str)
                except Exception as e:
                    print(f"Error converting raw balance '{raw_balance_str}' to Decimal for {address}: {e}")
                    return Decimal('0.0')

                # USDT TRC20 has 6 decimal places (1,000,000 sun per USDT)
                # Ensure division is also with Decimal for precision
                return raw_balance / Decimal('1000000') 
        
        # If loop completes and USDT token is not found for this address
        return Decimal('0.0')

    except requests.exceptions.Timeout:
        print(f"Error fetching balance for {address}: Request timed out after 10 seconds.")
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching balance for {address}: HTTP error {e.response.status_code} - {e.response.text}")
    except requests.exceptions.ConnectionError:
        print(f"Error fetching balance for {address}: Connection error (e.g., no internet).")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for {address}: An unexpected request error occurred: {e}")
    except ValueError as e: # Catch JSON decoding errors if resp.json() fails
        print(f"Error decoding JSON response for {address}: {e}. Response text: {resp.text[:200]}...")
    except Exception as e:
        print(f"An unexpected error occurred while fetching balance for {address}: {e}")
    
    return Decimal('0.0') # Return 0.0 on any error

def fetch_all_usdt_balances() -> tuple[str, dict[str, Decimal]]: # Type hints for return
    """
    Fetches USDT balances for all configured wallets.
    Prepares a formatted text summary message and returns the raw balances.

    Returns:
        tuple[str, dict[str, Decimal]]: A tuple containing:
            - str: A human-readable summary message including individual and total balances.
            - dict[str, Decimal]: A dictionary mapping wallet names to their USDT balances (Decimal).
    """
    # Fetch balances for each wallet. Using Decimal ensures precision throughout.
    balances = {name: get_usdt_trc20_balance(addr) for name, addr in WALLETS.items()}
    
    # Calculate total balance using Decimal objects
    total = sum(balances.values())

    # Get current time in GMT+7 for consistency
    gmt7_now = datetime.now(timezone(timedelta(hours=7)))
    time_str = gmt7_now.strftime("%Y-%m-%d %H:%M")

    # Prepare the lines for the Slack message
    lines = [
        f"*💵 USDT TRC20 Wallet Balances* 💵", # Added another emoji for flair
        f"_As of {time_str} GMT+7_",
        "" # Empty line for spacing
    ]

    for name, value in balances.items():
        # Format balance with comma thousands separator and two decimal places
        lines.append(f"• `{name}`: *{value:,.2f} USDT*")
    
    lines.append("") # Empty line for spacing
    lines.append(f"➕ *Total*: *{total:,.2f} USDT*")

    # Join all lines into a single message string
    return "\n".join(lines), balances