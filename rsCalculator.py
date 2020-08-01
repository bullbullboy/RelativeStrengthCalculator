import math
import Common

class Ticker:
    def __init__(self, idx, symbol, priceNow, price1QAgo, price2QAgo, price3QAgo, price4QAgo):
        self.invalid = (priceNow == '-') or (price1QAgo == '-') or (price2QAgo == '-') or (price3QAgo == '-') or (price4QAgo == '-')
        self.idx = idx
        self.symbol = symbol
        self.priceNow = priceNow
        self.price1QAgo = price1QAgo
        self.price2QAgo = price2QAgo
        self.price3QAgo = price3QAgo
        self.price4QAgo = price4QAgo
        self.RS = '-'

    def RSRawScore(self):
        priceNow = float(self.priceNow)
        price1QAgo = float(self.price1QAgo)
        price2QAgo = float(self.price2QAgo)
        price3QAgo = float(self.price3QAgo)
        price4QAgo = float(self.price4QAgo)
        return 2*priceNow / price1QAgo + priceNow / price2QAgo + priceNow / price3QAgo + priceNow / price4QAgo

    @classmethod
    # 銘柄    現在価格    3か月前価格  6か月前価格  9か月前価格  12か月前価格"フォーマットの文字列を受けてインスタンスを作成
    def createTicker(cls, idx, line):
        elem = line.split()
        if len(elem) < 6:
            raise ValueError
        else:
            return cls(idx, elem[0], elem[1], elem[2], elem[3], elem[4], elem[5])

def calcRS():
    #TODO 共通化
    PATH_RESULT = Common.pathOfPriceResult()
    PATH_RESULT_RS =Common.pathOfRSResult()

    # RS計算に必要な価格がかかれたファイルの読み込み
    # 各行は以下のフォーマット
    # 銘柄    現在価格    3か月前価格  6か月前価格  9か月前価格  12か月前価格
    with open(PATH_RESULT) as tickerListFile:
            tickerListFile.readline() #headerの読み捨て
            lines = tickerListFile.read()
    
    tickerList = []
    for count, line in enumerate(lines.split('\n')):
        #print(line)
        #print(count)
        try:
            tickerList.append(Ticker.createTicker(count, line))
        except ValueError:
            #do nothing
            break

    tickerListExcludeInvalidTicker = filter(lambda x: not x.invalid, tickerList)
    tickerListSortedByRSRawScore = sorted(tickerListExcludeInvalidTicker, key=lambda x: x.RSRawScore())

    # RS付与
    numOfTickers = len(tickerListSortedByRSRawScore)
    count = 0
    for eachTicker in tickerListSortedByRSRawScore:
        eachTicker.RS = math.floor((count / numOfTickers) * 100)
        count += 1
        # print(eachTicker.symbol + ':' + str(eachTicker.RS) + str(eachTicker.RSRawScore()))
    
    with open(PATH_RESULT_RS, mode='w') as f:
        for eachTicker in tickerList:
            f.write(eachTicker.symbol + '\t' + str(eachTicker.RS) + '\n')
