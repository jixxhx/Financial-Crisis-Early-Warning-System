import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime

print("Starting data collection process...")

start_date = "2000-01-01"
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

tickers = ['^GSPC', '^VIX', 'GC=F', 'CL=F']

try:
    print("Downloading market data (S&P500, VIX, Gold, Oil)...")
    # 수정됨: auto_adjust=True 옵션을 추가하고 'Close'를 가져옵니다.
    market_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
    
    # 데이터가 비어있는지 확인
    if market_data.empty:
        raise ValueError("Market data is empty.")
        
    market_data.columns = ['Oil', 'Gold', 'S&P500', 'VIX']
    print(">> Market data downloaded successfully.")
except Exception as e:
    print(f">> Error downloading market data: {e}")

try:
    print("Downloading economic indicators from FRED...")
    economic_data = web.DataReader(['T10Y2Y', 'DEXKOUS'], 'fred', start_date, end_date)
    print(">> Economic indicators downloaded successfully.")
except Exception as e:
    print(f">> Error downloading economic data: {e}")

if 'market_data' in locals() and 'economic_data' in locals():
    df = pd.concat([market_data, economic_data], axis=1)
    df = df.ffill().dropna()

    df.to_csv("financial_dataset.csv")

    print("\n------ Data Sample (Last 5 Days) ------")
    print(df.tail())
    print("\nSuccess! Data saved to 'financial_dataset.csv'.")
else:
    print("\nFailure: Could not collect all data.")