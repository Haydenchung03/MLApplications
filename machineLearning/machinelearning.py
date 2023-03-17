import pandas as pd
from matplotlib import pyplot
from pandas import set_option
from sys import path
from os import getcwd
path.append(getcwd())
import backTester as backTester
import vectorbt as vbt
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
class machineLearning(object):
    
    def __init__(self, tickers, start, end):
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
    
    

data1 = machineLearning(["MSFT", "AAPL"], "2023-03-10", "2023-03-17")