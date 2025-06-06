# bot/visualizer.py
"""
Module for visualizing cryptocurrency wallet balance trends.
Generates multi-panel plots (small multiples) for individual wallets,
displaying historical data and current balances in a clean, consistent format.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import math

# --- FIX: Import NUM_RECORDS_TO_PLOT from central configuration ---
from bot.config import NUM_RECORDS_TO_PLOT # <-- THIS WAS THE MISSING IMPORT

# Removed unused imports from datetime module that were commented out previously
# from datetime import timedelta, datetime, timezone 

def plot_wallet_trends(csv_path: str = "wallet_balances.csv", output_path: str = "wallet_trend.png") -> str | None:
    """
    Generates a multi-panel plot (small multiples) showing USDT wallet balance trends.
    Each wallet gets its own subplot with its current balance displayed in the title.
    Data is sourced from a CSV, and timestamps are consistently displayed in GMT+7.

    Args:
        csv_path (str): The file path to the CSV containing historical wallet balance data.
                        (Assumes 'Timestamp' column is ISO 8601 string with +07:00 offset).
        output_path (str): The file path where the generated chart image will be saved.

    Returns:
        str | None: The path to the saved image file if successful, otherwise None.
    """
    # NUM_RECORDS_TO_PLOT is now imported from bot.config.
    # No need to define it locally or pass it as an argument here.

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Error: CSV data file '{csv_path}' not found. Cannot plot trends.")
        return None
    except pd.errors.EmptyDataError:
        print(f"❌ Error: CSV data file '{csv_path}' is empty or malformed. Cannot plot trends.")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred while reading CSV '{csv_path}': {e}")
        return None

    if "Timestamp" not in df.columns:
        print(f"❌ Error: 'Timestamp' column not found in '{csv_path}'. Please check CSV header.")
        return None
    
    # --- Timestamp Processing for GMT+7 Display ---
    # CSV timestamps are like '2025-06-06T16:30:14+07:00'.
    # To ensure Matplotlib displays the *exact* '16:30' values without internal UTC conversion,
    # we strip the '+07:00' offset from the string BEFORE parsing to create NAIVE datetime objects.
    df["Timestamp"] = pd.to_datetime(df["Timestamp"].str.split('+').str[0]) 

    # Take the last 'NUM_RECORDS_TO_PLOT' unique time points, ensuring sorting by Timestamp.
    # Uses the imported NUM_RECORDS_TO_PLOT from config.
    df = df.drop_duplicates(subset=['Timestamp']).sort_values("Timestamp").tail(NUM_RECORDS_TO_PLOT)

    if df.empty:
        print(f"ℹ️ Not enough data points ({NUM_RECORDS_TO_PLOT} records) in '{csv_path}' to plot trends.")
        return None

    wallet_columns = df.columns[1:] # Get wallet names (excluding 'Timestamp')
    num_wallets = len(wallet_columns)

    # Determine optimal grid size for subplots (e.g., 2 columns, rows based on wallet count)
    num_cols = min(num_wallets, 2) 
    num_rows = math.ceil(num_wallets / num_cols)

    # --- Plot Setup ---
    plt.style.use('seaborn-v0_8-whitegrid') # Set a clean, white background style for the plots
    
    # Create the figure and subplots, sharing the X-axis for consistent time display across panels
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(6 * num_cols, 4 * num_rows), 
                             squeeze=False, sharex=True)
    
    axes = axes.flatten() # Flatten the axes array for easier iteration

    # Get the latest timestamp for the overall plot title (it's GMT+7 naive from processing)
    last_timestamp_gmt7_for_display = df['Timestamp'].iloc[-1]
    
    # Main title for the entire figure, explicitly stating GMT+7 for clarity
    fig.suptitle(
        f"USDT Wallet Balance Trend\n"
        f"({len(df)} Records as of {last_timestamp_gmt7_for_display.strftime('%Y-%m-%d %H:%M')} GMT+7)",
        fontsize=16, y=1.02 # Adjust y to ensure padding above subplots
    )

    # Prepare a categorical colormap for distinct line colors for each wallet
    colors = plt.cm.get_cmap('tab10', num_wallets)

    # --- Iterate through each wallet and create/populate its subplot ---
    for i, col in enumerate(wallet_columns):
        ax = axes[i] # Get the current subplot axis for this wallet
        
        last_value = df[col].iloc[-1] # Get the latest balance for the subplot title
        
        # Plot the line on the current subplot, using a unique color for the wallet
        # Only plot if there's any positive balance to avoid issues with empty scales.
        if last_value > 0 or df[col].max() > 0: 
            ax.plot(df["Timestamp"], df[col], marker="o", markersize=4, 
                    linewidth=1.2, color=colors(i)) 
        else:
            # If a wallet's balance is consistently zero, print a note and skip plotting its line
            print(f"Note: Wallet '{col}' has zero balance for all records. Line not plotted in chart.")

        # Set title for each subplot, including the wallet's name and its latest balance
        ax.set_title(f"{col}: {last_value:,.2f} USDT", fontsize=11, color='dimgray')
        
        # X-axis formatting for each subplot (labels only on bottom-most row due to sharex=True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15)) # Minor ticks for finer grid
        ax.tick_params(axis='x', rotation=0, labelsize=8) # Set tick label font size and rotation
        ax.tick_params(axis='y', labelsize=8)

        # Grid lines for each subplot
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_facecolor('white') # Ensure each subplot's background is white

    # Hide any unused subplots if the number of wallets doesn't perfectly fill the grid
    for i in range(num_wallets, len(axes)):
        fig.delaxes(axes[i])

    # --- Shared Axis Labels for the entire figure (best practice for small multiples) ---
    fig.supxlabel("Date and Time", fontsize=12, y=0.03) # Overall X-axis label
    fig.supylabel("USDT Balance", fontsize=12, x=0.04) # Overall Y-axis label

    # --- Adjust overall layout and save ---
    # `rect` adjusts the subplot area within the figure, leaving margins for suptitle and sup(x/y)label
    # `plt.tight_layout()` adjusts spacing between subplots for compactness.
    plt.tight_layout(rect=[0.05, 0.05, 0.98, 0.98]) 

    output_path = str(Path(output_path))
    try:
        plt.savefig(output_path, dpi=300, bbox_inches="tight") # Save with high DPI and tight bounding box
        print(f"✅ Chart saved to {output_path}")
    except Exception as e:
        print(f"❌ Error saving chart to {output_path}: {e}")
        return None
    finally:
        plt.close(fig) # Always close the figure to free up memory, especially in cron jobs

    return output_path