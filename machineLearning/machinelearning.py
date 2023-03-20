from pandas import set_option
from sys import path
from os import getcwd
path.append(getcwd())
import backTester.backTester as backTester
import vectorbt as vbt

#Function and modules for data preparation and visualization
import numpy as np
import pandas as pd
import pandas_datareader.data as web

class machineLearning(object):
    
    def __init__(self, tickers, start, end):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.vectorBT = backTester.BackTester.VectorBT(tickers, start, end)

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
        getDayData = []
        for i in range(len(self.tickers)):
            getDayData.append(backTester.BackTester.AlphaVantage(self.tickers[i], self.start, self.end).getDayData())
        
        getDayData = pd.DataFrame(getDayData)
        

        ccy_data = web.DataReader(exchangeRates_prices, 'fred', start = self.start, end = self.end)
        idx_data = web.DataReader(index_tickers, 'fred', start = self.start, end = self.end)
        print(getDayData.to_string())


machineLearning(['MSFT', 'AAPL'], "2023-03-05", "2023-03-17").predictStockPrice(['DEXJPUS', 'DEXUSUK'], ['SP500', 'DJIA', 'VIXCLS'])


