import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Get trending stocks from user input
trending_stocks_input = input("Enter trending stock symbols separated by commas (e.g., TCS.NS,NVDA,TSLA): ")
trending_stocks = [symbol.strip() for symbol in trending_stocks_input.split(",")]

# Modified data fetching function
def get_stock_data(symbol, period='1y'):
    try:
        # Download historical data
        data = yf.download(symbol, period=period, progress=False, auto_adjust=True)
        
        if data.empty:
            print(f"No data found for {symbol}")
            return pd.Series()
            
        # Use Close price (already auto-adjusted)
        price_series = data['Close']
        
        # Calculate returns
        returns = price_series.pct_change().dropna()
        
        if returns.empty:
            print(f"Insufficient data to calculate returns for {symbol}")
            return pd.Series()
            
        return returns
    
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")
        return pd.Series()

# Anomaly detection using Z-Score
def zscore_anomaly_detection(data, threshold=3):
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold

# Anomaly detection using Isolation Forest
def isolation_forest_anomaly_detection(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))
    
    model = IsolationForest(contamination=0.05, random_state=42)
    predictions = model.fit_predict(scaled_data)
    
    return pd.DataFrame(predictions == -1, index=data.index, columns=data.columns)

def analyze_stocks(stock_symbols):
    results = {}
    
    for symbol in stock_symbols:
        print(f"\nAnalyzing {symbol}...")
        returns = get_stock_data(symbol)
        
        if returns.empty:
            print(f"Skipping {symbol} due to data issues")
            continue
            
        # Detect anomalies
        zscore_anomalies = zscore_anomaly_detection(returns)
        isolation_anomalies = isolation_forest_anomaly_detection(returns)
        
        print(f'{symbol} returns shape: {returns.shape}')
        print(f'{symbol} zscore_anomalies shape: {zscore_anomalies.shape}')
        print(f'{symbol} isolation_anomalies shape: {isolation_anomalies.shape}')
        
        anomalies = returns[zscore_anomalies | isolation_anomalies]
        
        # Store results
        results[symbol] = {
            'returns': returns,
            'anomalies': anomalies,
            'zscore_anomalies': zscore_anomalies.sum(),
            'isolation_anomalies': isolation_anomalies.sum().sum()
        }
        
        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(returns.index, returns, label='Daily Returns')
        plt.scatter(anomalies.index, anomalies, color='red', label='Anomalies')
        plt.title(f"{symbol} Price Returns with Anomalies")
        plt.legend()
        plt.show()
        
    return results

# Execute analysis
analysis_results = analyze_stocks(trending_stocks)

# Summary report
print("\nAnomaly Summary Report:")
for symbol, result in analysis_results.items():
    if result is None or not all(key in result for key in ['returns', 'anomalies', 'zscore_anomalies', 'isolation_anomalies']):
        print(f"Skipping {symbol} due to unexpected data format.")
        continue
    print(f"\n{symbol}:")
    print(f"Analysis period: {result['returns'].index[0].date()} to {result['returns'].index[-1].date()}")
    print(f"Total anomalies detected: {len(result['anomalies'])}")
    print(f"Most recent anomalies: {result['anomalies'].index[-3:].strftime('%Y-%m-%d').tolist() if len(result['anomalies']) > 0 else 'None'}")