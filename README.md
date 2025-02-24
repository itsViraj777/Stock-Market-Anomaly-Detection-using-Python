# Stock-Market-Anomaly-Detection-using-Python
This project focuses on detecting anomalies in stock market data using Python. It leverages two popular anomaly detection techniques: Z-Score and Isolation Forest. The project is designed to analyze stock price returns and identify unusual patterns that may indicate significant market events or data irregularities.
Features
Data Fetching: Fetches historical stock data using the yfinance library.

# Anomaly Detection:

- Z-Score: Detects anomalies based on the standard deviation of stock returns.

- Isolation Forest: Uses an unsupervised machine learning algorithm to identify outliers.

- Visualization: Plots stock returns and highlights detected anomalies.

- User Input: Allows users to input multiple stock symbols for analysis.

Requirements
To run this project, you need the following Python libraries:

- yfinance

- pandas

- numpy

- matplotlib

- scikit-learn

You can install the required libraries using pip:

```
pip install yfinance pandas numpy matplotlib scikit-learn
```
Usage
Clone the repository or download the script.

Run the script:

```
python stock_anomaly_detection.py
```
Input Stock Symbols:

When prompted, enter the stock symbols you want to analyze, separated by commas. For example:

Enter trending stock symbols separated by commas (e.g., TCS.NS,NVDA,TSLA): TCS.NS,NVDA,TSLA
View Results:

The script will:

Fetch historical data for the specified stocks.

Detect anomalies using both Z-Score and Isolation Forest methods.

Plot the stock returns with anomalies highlighted.

Print a summary report of detected anomalies.

# Code Overview
Data Fetching
The get_stock_data function fetches historical stock data using the yfinance library. It calculates daily returns and handles errors gracefully.

```
def get_stock_data(symbol, period='1y'):
    try:
        data = yf.download(symbol, period=period, progress=False, auto_adjust=True)
        if data.empty:
            print(f"No data found for {symbol}")
            return pd.Series()
        price_series = data['Close']
        returns = price_series.pct_change().dropna()
        if returns.empty:
            print(f"Insufficient data to calculate returns for {symbol}")
            return pd.Series()
        return returns
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")
        return pd.Series()
```
Anomaly Detection
Z-Score: The zscore_anomaly_detection function calculates the Z-Score for the stock returns and identifies anomalies based on a specified threshold.

python
Copy
def zscore_anomaly_detection(data, threshold=3):
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold
Isolation Forest: The isolation_forest_anomaly_detection function uses the Isolation Forest algorithm to detect anomalies.

python
Copy
def isolation_forest_anomaly_detection(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))
    model = IsolationForest(contamination=0.05, random_state=42)
    predictions = model.fit_predict(scaled_data)
    return pd.DataFrame(predictions == -1, index=data.index, columns=data.columns)
Visualization
The script plots the stock returns and highlights the detected anomalies using matplotlib.

python
Copy
plt.figure(figsize=(12, 6))
plt.plot(returns.index, returns, label='Daily Returns')
plt.scatter(anomalies.index, anomalies, color='red', label='Anomalies')
plt.title(f"{symbol} Price Returns with Anomalies")
plt.legend()
plt.show()
Summary Report
After analyzing all the stocks, the script prints a summary report detailing the number of anomalies detected and the most recent anomalies.

python
Copy
print("\nAnomaly Summary Report:")
for symbol, result in analysis_results.items():
    print(f"\n{symbol}:")
    print(f"Analysis period: {result['returns'].index[0].date()} to {result['returns'].index[-1].date()}")
    print(f"Total anomalies detected: {len(result['anomalies'])}")
    print(f"Most recent anomalies: {result['anomalies'].index[-3:].strftime('%Y-%m-%d').tolist() if len(result['anomalies']) > 0 else 'None'}")
Example Output
Copy
Analyzing TCS.NS...
TCS.NS returns shape: (252,)
TCS.NS zscore_anomalies shape: (252,)
TCS.NS isolation_anomalies shape: (252, 1)

Analyzing NVDA...
NVDA returns shape: (252,)
NVDA zscore_anomalies shape: (252,)
NVDA isolation_anomalies shape: (252, 1)

Analyzing TSLA...
TSLA returns shape: (252,)
TSLA zscore_anomalies shape: (252,)
TSLA isolation_anomalies shape: (252, 1)

Anomaly Summary Report:

TCS.NS:
Analysis period: 2022-10-03 to 2023-10-02
Total anomalies detected: 12
Most recent anomalies: ['2023-09-28', '2023-09-29', '2023-10-02']

NVDA:
Analysis period: 2022-10-03 to 2023-10-02
Total anomalies detected: 10
Most recent anomalies: ['2023-09-28', '2023-09-29', '2023-10-02']

TSLA:
Analysis period: 2022-10-03 to 2023-10-02
Total anomalies detected: 15
Most recent anomalies: ['2023-09-28', '2023-09-29', '2023-10-02']
