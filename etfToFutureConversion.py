import yfinance as yf
import numpy as np
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")

def get_intraday_prices(ticker, interval="15m"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2d", interval=interval, prepost=True)
    return hist['Close']

def calculate_conversion_ratios(price_series1, price_series2):
    # Ensure both series have the same length
    min_length = min(len(price_series1), len(price_series2))
    price_series1 = price_series1[-min_length:]
    price_series2 = price_series2[-min_length:]
    
    # Calculate conversion ratios
    conversion_ratios = price_series1 / price_series2
    return conversion_ratios

def get_latest_conversion_ratios(conversion_ratios, n):
    return conversion_ratios[-n:]

def calculate_average_ratio(conversion_ratios):
    return np.mean(conversion_ratios)

def convert_price(input_price, conversion_ratio):
    return input_price / conversion_ratio

def round_to_nearest_tick(price, tick_size=0.25):
    return round(price / tick_size) * tick_size

def main():
    conversion_choice = input("Do you want to convert SPY to MES, QQQ to MNQ, IWM to RTY, or DIA to MYM? Enter 'SPY', 'QQQ', 'IWM', or 'DIA': ").strip().upper()
    
    if conversion_choice == 'SPY':
        input_price = float(input("Enter the SPY price to convert: "))
        ticker1, ticker2 = "SPY", "MES=F"
    elif conversion_choice == 'QQQ':
        input_price = float(input("Enter the QQQ price to convert: "))
        ticker1, ticker2 = "QQQ", "MNQ=F"
    elif conversion_choice == 'IWM':
        input_price = float(input("Enter the IWM price to convert: "))
        ticker1, ticker2 = "IWM", "RTY=F"
    elif conversion_choice == 'DIA':
        input_price = float(input("Enter the DIA price to convert: "))
        ticker1, ticker2 = "DIA", "MYM=F"
    else:
        print("Invalid choice. Please enter 'SPY', 'QQQ', 'IWM', or 'DIA'.")
        return

    # Retrieve intraday prices
    prices1 = get_intraday_prices(ticker1)
    prices2 = get_intraday_prices(ticker2)

    # Calculate conversion ratios
    conversion_ratios = calculate_conversion_ratios(prices1, prices2)
    
    # Get the last 10 conversion ratios
    latest_conversion_ratios = get_latest_conversion_ratios(conversion_ratios, n=10)
    
    # Calculate the average of the last 10 conversion ratios
    average_conversion_ratio = calculate_average_ratio(latest_conversion_ratios)
    
    # Convert input price to the other asset price
    converted_price = convert_price(input_price, average_conversion_ratio)

    # Round the converted price to the nearest tick
    rounded_converted_price = round_to_nearest_tick(converted_price)
    
    print(f"The equivalent {ticker2} price for {ticker1} price {input_price} is {rounded_converted_price:.2f} with a conversion multiplier of {(1 / average_conversion_ratio):.4f}\n")

if __name__ == "__main__":
    main()
