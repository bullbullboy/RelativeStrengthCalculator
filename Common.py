import os

def pathOfPriceResult():
    return os.path.dirname(__file__) + '/resultPrice.txt'

def pathOfRSResult():
    return os.path.dirname(__file__) + '/resultRS.txt'

def pathOfTickerList():
    return os.path.dirname(__file__) + '/tickerList.txt'
