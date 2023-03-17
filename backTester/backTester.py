import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import vectorbt as vbt
import yfinance as yf

from alpha_vantage.timeseries import TimeSeries
from decouple import config
import datetime
from datetime import date, timedelta


class BackTester(object):

    class AlphaVantage(object):
        def __init__(self, ticker, start, end):
            self.key = config('ALPHA_ADVANTAGE')
            self.ticker = ticker
            self.start = start
            self.end = end

        
        # This function is used to get information such as open, high, low, close, adjusted close, volume, dividend amount, and split coefficient of a ticker 
        # between a given start and end date.
        def getDayData(self):
            data = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&outputsize=full&apikey={self.key}"
            data = pd.read_json(data)
            returnData = {}
            
            startYear = int(self.start[0:4])
            startMonth = int(self.start[5:7])
            startDay = int(self.start[8:10])

            endYear = int(self.end[0:4])
            endMonth = int(self.end[5:7])
            endDay = int(self.end[8:10])

            start_date = date(startYear, startMonth, startDay)
            end_date = date(endYear, endMonth, endDay)

            delta = timedelta(days=1)
            while start_date <= end_date:

            
                try:
                    
                    dayData = data['Time Series (Daily)'][str(start_date)]
                    returnData[str(start_date)] = dayData
                    
                    start_date += delta
                except:
                    start_date += delta
                    continue
            return returnData
        
        # This function will print out the data for the function above.
        def printDayData(self):
            data = BackTester.getDayData(self)
            print(f"Data for {self.ticker} between {self.start} and {self.end}:")
            for key in data:
                print(f"{key}: {data[key]}")
    
    class VectorBT(object):
        def __init__(self, ticker, start, end):
            self.tickers = ticker
            self.start = start
            self.end = end

        # This function will take close prices and return a list of the RSI values for each day. Windows are considered "candles"

        def customIndicator(self, close, rsi_window = 14, ma_window = 50):
            # Resample the data to 5 minute intervals and take the last value of each interval.
            close_5m = close.resample('5min').last()
            # Relative strength index
            rsi = vbt.RSI.run(close_5m, window = [rsi_window]).rsi
            # Align the RSI values with the data sets. Example(Lines up minute data with 5 min data.) 
            # Forwards fill the RSI values if there is no data for that candle.
            # This means that the rsi and close values will be in the exact same size
            rsi, _ = rsi.align(close, broadcast_axis = 0, method = 'ffill', join = 'right')
            
            close = close.to_numpy()
            rsi = rsi.to_numpy()
            # Moving average based on closing prices
            ma = vbt.MA.run(close, window = [ma_window]).ma.to_numpy()

            # If it is above 70, exit the position. If it is below 30, enter the position. If it is between 30 and 70, do nothing. 
            # Only buy if the closing price is below the moving average.
            trend = np.where(rsi > 70, -1, 0)
            trend = np.where((rsi < 30) & (close < ma), 1, trend)
            return trend
            

        # This function will take the custom indicator function and return a list of the RSI values for each day.
        def indicatorFactory(self):
            ticker_prices = vbt.YFData.download(self.tickers, missing_index = 'drop', start = self.start, end = self.end, interval = "1m").get('Close')
            # indicator factory
            indicator = vbt.IndicatorFactory(
                class_name = "Combination",
                short_name = "comb",
                input_names = ["close"],
                param_names = ["rsi_window", "ma_window"],
                output_names = ["value"]
            ).from_apply_func(
                self.customIndicator,
                rsi_window = 14,
                ma_window = 50,
                keep_pd = True
            )
            # Testing out the function above
            comb = indicator.run(ticker_prices, rsi_window = 21, ma_window = 50)
            return [ticker_prices, comb]
        
        # This returns a percentage of total returns and losses for each ticker
        def portfolioStats(self):
            indicatoryInfo = self.indicatorFactory()
            
            ticker_prices = indicatoryInfo[0]
            comb = indicatoryInfo[1]
            # Entries and exits that returns a boolean value
            entries = comb.value == 1.0
            exits = comb.value == -1.0
            porfolio = vbt.Portfolio.from_signals(ticker_prices, entries, exits)
            return porfolio.total_return()

        # This function returns indicator values for each ticker given a time interval, start date, and end date
        def indicatorValues(self):
            indicatoryInfo = self.indicatorFactory()
            comb = indicatoryInfo[1]
            # 0 means do nothing, 1 means buy, -1 means sell. Based on the RSI values and the moving average.
            return comb.value.to_string()

    


test = BackTester.VectorBT(["MSFT", "AAPL"], "2023-03-10", "2023-03-17")
print(test.indicatorValues())
print(test.portfolioStats())
