import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def plot_wallet_trends(csv_path="wallet_history.csv", output_path="wallet_trend.png"):
    df = pd.read_csv(csv_path)
    df["Time"] = pd.to_datetime(df["Time"])
    df = df.sort_values("Time").tail(13)

    plt.figure(figsize=(12, 6))

    shown_labels = set()  # Track which final values are already labeled

    for col in df.columns[1:]:
        plt.plot(df["Time"], df[col], marker="o", markersize=4, label=col)

        # Label only unique final values
        last_x = df["Time"].iloc[-1]
        last_y = df[col].iloc[-1]
        if last_y not in shown_labels:
            shown_labels.add(last_y)

            # Offset label for readability
            x_offset = pd.Timedelta(minutes=0.01)
            y_offset = -(df[col].max() - df[col].min()) * 0.03

            plt.text(
                last_x + x_offset,
                last_y + y_offset,
                f"{last_y:.0f}",
                fontsize=9, va="top", ha="left", color="black"
            )

    plt.title("Wallet Balance Trend (Last 13 Records)", fontsize=14)
    plt.xlabel("Time (GMT+7)")
    plt.ylabel("TRX")

    # Format X-axis
    plt.xticks(df["Time"], rotation=0)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d\n%H:%M'))

    # Light grid
    plt.grid(True, linestyle="--", linewidth=0.4, alpha=0.2)

    # External legend
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)

    plt.tight_layout()
    output_path = str(Path(output_path))
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"✅ Chart saved to {output_path}")
    return output_path
