from pandas import set_option
from sys import path
from os import getcwd
path.append(getcwd())
import backTester.backTester as backTester
import vectorbt as vbt

#Function and modules for data preparation and visualization
# pandas, pandas_datareader, numpy and matplotlib
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from matplotlib import pyplot

class machineLearning(object):
    
    def __init__(self, tickers, start, end, interval):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.interval = interval
        self.vectorBT = backTester.BackTester.VectorBT(tickers, start, end, interval)

    def returnDataStatistics(self):

        data = self.vectorBT.indicatorFactoryScores()
        set_option('display.width', 100)
        set_option('display.precision', 3)
        #print(''' Summarizing buy signals for each ticker''')
        #print(''' Summarzing moving average for each ticker''')
        return [data[0].describe(), data[1].describe()]
    
    def returnTrendStatistics(self):

        data = self.vectorBT.indicatorFactory()
        set_option('display.width', 100)
        set_option('display.precision', 3)
        #print(''' Summarizing buy/sell signal trends for each ticker''')
        print(data[1].describe())
        return data[1].describe()

    def predictStockPrice(self, exchangeRates_prices, index_tickers):
        
        stx_data = self.vectorBT.getRawPrices()
    
        ccy_data = web.DataReader(exchangeRates_prices, 'fred', start = self.start, end = self.end)
        idx_data = web.DataReader(index_tickers, 'fred', start = self.start, end = self.end)


machineLearning(['MSFT', 'AAPL'], "2023-03-13", "2023-03-18", "1m").predictStockPrice(['DEXJPUS', 'DEXUSUK'], ['SP500', 'DJIA', 'VIXCLS'])


