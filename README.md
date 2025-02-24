# Stock-Market-Anomaly-Detection-using-Python
This project focuses on detecting anomalies in stock market data using Python. It leverages two popular anomaly detection techniques: Z-Score and Isolation Forest. The project is designed to analyze stock price returns and identify unusual patterns that may indicate significant market events or data irregularities.
Features
Data Fetching: Fetches historical stock data using the yfinance library.

# Anomaly Detection:

- Z-Score: Detects anomalies based on the standard deviation of stock returns.

- Isolation Forest: Uses an unsupervised machine learning algorithm to identify outliers.

- Visualization: Plots stock returns and highlights detected anomalies.

- User Input: Allows users to input multiple stock symbols for analysis.

# Requirements
To run this project, you need the following Python libraries:

- yfinance

- pandas

- numpy

- matplotlib

- scikit-learn

## You can install the required libraries using pip:

```
pip install yfinance pandas numpy matplotlib scikit-learn
```

## Clone the repository or download the script.
```
git clone https://github.com/your-username/stock-market-anomaly-detection.git
cd stock-market-anomaly-detection
```
## Run the script:

```
python stock_anomaly_detection.py
```
## Input Stock Symbols:

When prompted, enter the stock symbols you want to analyze, separated by commas. For example:

Enter trending stock symbols separated by commas (e.g., TCS.NS,NVDA,TSLA): TCS.NS,NVDA,TSLA
View Results:

The script will:

Fetch historical data for the specified stocks.

Detect anomalies using both Z-Score and Isolation Forest methods.

Plot the stock returns with anomalies highlighted.

Print a summary report of detected anomalies.

