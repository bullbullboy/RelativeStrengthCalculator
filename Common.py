import os

def pathOfResultDir():
    return os.path.dirname(__file__) + '/result'

def pathOfPriceResult():
    return pathOfResultDir() + '/resultPrice.txt'

def pathOfRSResult():
    return  pathOfResultDir() + '/resultRS.txt'

def pathOfTickerList():
    return os.path.dirname(__file__) + '/tickerList.txt'

def pathOfDebug():
    return os.path.dirname(__file__) + '/debug.txt'