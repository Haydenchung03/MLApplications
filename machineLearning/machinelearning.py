import pandas as pd
from matplotlib import pyplot
from pandas import set_option
from sys import path
from os import getcwd
path.append(getcwd())
import backTester.backTester as backTester
import vectorbt as vbt
class machineLearning():
    
    def __init__(self):
        pass

    def plotData(self):
        backTesting = backTester.BackTester()

        data = backTesting.VectorBT(["MSFT", "AAPL"], "2023-03-10", "2023-03-17").indicatorFactoryScores()
        set_option("display.width", 100)
        print(data[0].tail(1))
        print(data[1].head(1))

machineLearning().plotData()