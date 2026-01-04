import pandas as pd
import matplotlib.pyplot as plt

print("Starting data visualization...")

try:
    # 1. Load Data
    df = pd.read_csv('financial_dataset.csv', index_col=0, parse_dates=True)
    print(">> Data loaded successfully.")
    
    # 2. Setup Plot Style
    plt.style.use('bmh')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 3. Plot S&P 500 (Left Axis)
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('S&P 500 Price', color=color, fontsize=12)
    ax1.plot(df.index, df['S&P500'], color=color, linewidth=2, label='S&P 500')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    # 4. Plot VIX (Right Axis)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('VIX (Fear Index)', color=color, fontsize=12)
    ax2.plot(df.index, df['VIX'], color=color, linewidth=1, linestyle='--', alpha=0.7, label='VIX')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.grid(False)

    # 5. Finalize and Save
    plt.title('Market Overview: S&P 500 vs VIX (Fear Index)', fontsize=16, fontweight='bold')
    fig.tight_layout()
    
    plt.savefig('market_overview.png', dpi=300)
    print(">> Graph saved as 'market_overview.png'")
    
    plt.show() 

except Exception as e:
    print(f"Error: {e}")