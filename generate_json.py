import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from dotenv import load_dotenv
import os


# Define various variables
load_dotenv()
api_key = os.getenv("COINGECKO_API_KEY")

charts_path = './crypto_charts/'

tickers_to_watch = {
    "bitcoin": {"token": "BTC", "name": "Bitcoin (BTC)", "color": "orange"},
    "ethereum": {"token": "ETH", "name": "Ethereum (ETH)", "color": "gray"},
    "axie-infinity": {"token": "AXS", "name": "Axie (AXS)", "color": "darkblue"},
    "smooth-love-potion": {"token": "SLP", "name": "SLP", "color": "hotpink"},
    "ronin": {"token": "RON", "name": "Ronin (RON)", "color": "blue"},
    "solana": {"token": "SOL", "name": "Solana (SOL)", "color": "lime"},
    "myria": {"token": "MYRIA", "name": "Myria (MYRIA)", "color": "navy"},
    "chainlink": {"token": "LINK", "name": "Chainlink (LINK)", "color": "cyan"},
}

token_pairs = [
    ('bitcoin','ethereum'),
    ('axie-infinity','ronin')
]


# function to get the pandas dataframe with prices of a ticker per day, for the selected previous days
def get_market_chart(ticker, currency='eur', days='30', interval='daily'):
    url = f'https://api.coingecko.com/api/v3/coins/{ticker}/market_chart?vs_currency={currency}&days={days}&interval={interval}'
    headers = { "x-cg-demo-api-key": api_key }
    response = requests.get(url, headers=headers)
    df = pd.DataFrame(json.loads(response.text)['prices'], columns=['datetime','price'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    return df


# function to get the pandas dataframe with the ohlc data of a ticker per day, for the selected previous days
def get_ohlc(ticker, currency='eur', days='30'):
    url = f'https://api.coingecko.com/api/v3/coins/{ticker}/ohlc?vs_currency={currency}&days={days}'
    headers = { "x-cg-demo-api-key": api_key }
    response = requests.get(url, headers=headers)
    r = pd.DataFrame(json.loads(response.text), columns=['timestamp','open','high','low','close'])
    #r = r.rename(columns={"time_period_end": "CloseTime", "price_close": "ClosePrice"})
    return json.loads(response.text)


# function generate a 2 lines plot to compare 2 tickers and save it to disk as a png image
def generate_2_line_plot(x_series1, y_series1, color1, label1, ylabel1, x_series2, y_series2, color2, label2, ylabel2, plot_path):
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ax.tick_params(axis='x', labelsize=8, rotation=30)
    ax.plot(x_series1, y_series1, color=color1, label=label1)
    ax.set_ylabel(ylabel1)
    plt.grid(color='gray', linestyle='dotted', linewidth=1)
    ax2 = ax.twinx()
    ax2.plot(x_series2, y_series2, color=color2, label=label2)
    ax2.set_ylabel(ylabel2)
    fig.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(plot_path)
    return


# function generate a lines plot to and save it to disk as a png image
def generate_1_line_plot(x_series, y_series, color, ylabel, plot_path):
    plt.figure(figsize=(4.5, 4))
    plt.tick_params(axis='x', labelsize=8, rotation=30)
    plt.plot(x_series, y_series, color=color)
    plt.ylabel(ylabel)
    plt.grid(color='gray', linestyle='dotted', linewidth=1)
    plt.tight_layout()
    plt.savefig(plot_path)
    return



# main function
def main():
    tickers_info = []

    # generate charts for the double line plots (comparing 2 tokens)
    for (ticker1 , ticker2) in token_pairs:
        data1 = get_market_chart(ticker1, days='30')
        data2 = get_market_chart(ticker2, days='30')
        figure_path = charts_path + tickers_to_watch[ticker1]['token'] + '_' + tickers_to_watch[ticker2]['token'] + '.png'
        generate_2_line_plot(
            data1['datetime'],
            data1['price'],
            tickers_to_watch[ticker1]['color'],
            tickers_to_watch[ticker1]['token'],
            tickers_to_watch[ticker1]['name'] + " [EUR]",
            data2['datetime'],
            data2['price'],
            tickers_to_watch[ticker2]['color'],
            tickers_to_watch[ticker2]['token'],
            tickers_to_watch[ticker2]['name'] + " [EUR]",
            figure_path
        )
        tickers_info.append({
            "ticker": '',
            "figure_path": figure_path,
            "title": tickers_to_watch[ticker1]['name'] + " vs. " + tickers_to_watch[ticker2]['name'] + " Chart"
            })

    # generate charts for the single line plots
    for ticker in tickers_to_watch:
        if ticker in ['bitcoin','ethereum','axie-infinity','smooth-love-potion']:
            continue
        data = get_market_chart(ticker, days='30')
        figure_path = charts_path + tickers_to_watch[ticker]['token'] + '.png'
        generate_1_line_plot(
            data['datetime'],
            data['price'],
            tickers_to_watch[ticker]['color'],
            tickers_to_watch[ticker]['name'] + " [EUR]",
            figure_path
        )
        tickers_info.append({
            "ticker": ticker,
            "figure_path": figure_path,
            "title": tickers_to_watch[ticker]['name'] + " Chart"
            })

    # Save information into json file
    with open("./references/tickers_info.json", "w") as f:
        json.dump(tickers_info, f, indent=2)
    print("Generated json file")


if __name__ == "__main__":
    main()