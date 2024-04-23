import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Function to download stock data
def download_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to calculate basic statistics
def calculate_statistics(stock_data):
    statistics = {
        'Mean': stock_data['Close'].mean(),
        'Std Dev': stock_data['Close'].std(),
        'Min': stock_data['Close'].min(),
        'Max': stock_data['Close'].max(),
        'Median': stock_data['Close'].median(),
    }
    return statistics

# Function to calculate moving averages
def calculate_moving_averages(stock_data, short_window=20, long_window=50):
    stock_data['Short_MA'] = stock_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    stock_data['Long_MA'] = stock_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(stock_data, window=20, num_std_dev=2):
    stock_data['Rolling_Mean'] = stock_data['Close'].rolling(window=window, min_periods=1, center=False).mean()
    stock_data['Upper_Band'] = stock_data['Rolling_Mean'] + (stock_data['Close'].rolling(window=window, min_periods=1, center=False).std() * num_std_dev)
    stock_data['Lower_Band'] = stock_data['Rolling_Mean'] - (stock_data['Close'].rolling(window=window, min_periods=1, center=False).std() * num_std_dev)

# Function to calculate daily returns
def calculate_daily_returns(stock_data):
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()

# Function to perform basic trend analysis
def trend_analysis(stock_data):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=stock_data.index, y=stock_data['Close'], label='Close Price')
    sns.lineplot(x=stock_data.index, y=stock_data['Short_MA'], label='Short MA')
    sns.lineplot(x=stock_data.index, y=stock_data['Long_MA'], label='Long MA')
    sns.lineplot(x=stock_data.index, y=stock_data['Upper_Band'], label='Upper Band')
    sns.lineplot(x=stock_data.index, y=stock_data['Lower_Band'], label='Lower Band')
    plt.title('Stock Price Trend Analysis with Moving Averages and Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

# Function to implement a basic moving average crossover strategy
def moving_average_crossover_strategy(stock_data):
    stock_data['Signal'] = 0  # 0: No Signal, 1: Buy Signal, -1: Sell Signal

    # Generate signals
    stock_data.loc[stock_data['Short_MA'] > stock_data['Long_MA'], 'Signal'] = 1
    stock_data.loc[stock_data['Short_MA'] < stock_data['Long_MA'], 'Signal'] = -1

    # Generate suggestions
    stock_data['Recommendation'] = ''
    stock_data.loc[stock_data['Signal'] == 1, 'Recommendation'] = 'Buy'
    stock_data.loc[stock_data['Signal'] == -1, 'Recommendation'] = 'Sell'

# Function to display trading signals and recommendations
def display_trading_signals(stock_data):
    plt.figure(figsize=(12, 8))
    plt.plot(stock_data['Close'], label='Close Price')
    plt.plot(stock_data['Short_MA'], label='Short MA')
    plt.plot(stock_data['Long_MA'], label='Long MA')

    # Plot Buy signals
    plt.plot(stock_data[stock_data['Signal'] == 1].index,
             stock_data['Short_MA'][stock_data['Signal'] == 1],
             '^', markersize=10, color='g', label='Buy Signal')

    # Plot Sell signals
    plt.plot(stock_data[stock_data['Signal'] == -1].index,
             stock_data['Short_MA'][stock_data['Signal'] == -1],
             'v', markersize=10, color='r', label='Sell Signal')

    plt.title('Stock Price with Buy/Sell Signals based on Moving Average Crossover')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

    # Display recommendations
    recommendations = stock_data.loc[stock_data['Recommendation'] != ''].copy()
    print('\nTrading Recommendations:')
    print(recommendations[['Recommendation', 'Close']])

# Main function for stock analysis with predictive code
def stock_analysis_with_prediction(ticker, start_date, end_date):
    stock_data = download_stock_data(ticker, start_date, end_date)

    if stock_data.empty:
        print(f'No data available for {ticker} in the specified date range.')
        return

    # Calculate additional metrics
    calculate_moving_averages(stock_data)
    calculate_bollinger_bands(stock_data)
    calculate_daily_returns(stock_data)

    # Implement basic moving average crossover strategy
    moving_average_crossover_strategy(stock_data)

    # Display basic statistics
    statistics = calculate_statistics(stock_data)
    print(f'\nBasic Statistics for {ticker} Stock:\n')
    for stat, value in statistics.items():
        print(f'{stat}: {value}')

    # Plot stock data
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price')
    plt.title(f'{ticker} Stock Price Analysis')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()

    # Perform trend analysis
    trend_analysis(stock_data)

    # Display trading signals and recommendations
    display_trading_signals(stock_data)

# Example usage
if __name__ == "__main__":
    # Get user input for stock ticker
    ticker = input("Enter the stock ticker (e.g., AAPL): ").upper()

    # Set start date and end date
    start_date = "2022-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Run stock analysis with prediction for the specified stock
    stock_analysis_with_prediction(ticker, start_date, end_date)
