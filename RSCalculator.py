import math
import Common

class Ticker:
    def __init__(self, idx, symbol, priceNow, price1QAgo, price2QAgo, price3QAgo, price4QAgo):
        #self.invalid = (priceNow == '-') or (price1QAgo == '-') or (price2QAgo == '-') or (price3QAgo == '-') or (price4QAgo == '-')
        self.invalid = False
        self.idx = idx
        self.symbol = symbol

        try:
            self.priceNow = float(priceNow)
            self.price1QAgo = float(price1QAgo)
            self.price2QAgo = float(price2QAgo)
            self.price3QAgo = float(price3QAgo)
            self.price4QAgo = float(price4QAgo)
        except:
            self.invalid = True

        self.RS = '-'
        self.RSRaw = self.RSRawScore()

    def RSRawScore(self):
        try:
            score = 2 * self.priceNow / self.price1QAgo + self.priceNow / self.price2QAgo + self.priceNow / self.price3QAgo + self.priceNow / self.price4QAgo
            if math.isnan(score):
                self.invalid = True
        except:
            score = '-'
            self.invalid = True
    
        return score

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
    PATH_DEBUG = Common.pathOfDebug()

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

    #print(str(len(tickerList)) + '\n')
    tickerListExcludeInvalidTicker = filter(lambda x: not x.invalid, tickerList)

    # with open(PATH_DEBUG, mode='w') as f:
    #     for eachTicker in tickerListExcludeInvalidTicker:
    #         f.write(eachTicker.symbol + '\n')
    #print(str(len(list(tickerListExcludeInvalidTicker))))
    
    tickerListSortedByRSRawScore = sorted(tickerListExcludeInvalidTicker, key=lambda x: x.RSRaw)
    #print("result" + str(len(tickerListSortedByRSRawScore)) + '\n')

    # RS付与
    numOfTickers = len(tickerListSortedByRSRawScore)
    count = 0

    with open(PATH_RESULT_RS, mode='w') as f:
        for eachTicker in tickerListSortedByRSRawScore:
            eachTicker.RS = min(math.floor((count / numOfTickers) * 99) + 1, 99)
            count += 1
            f.write(eachTicker.symbol + '\t' + str(eachTicker.RS) + '\t' + str(eachTicker.RSRaw) + '\n')
            #print(eachTicker.symbol + ':' + str(eachTicker.RS) + '\t' + str(eachTicker.RSRawScore()))
    
    with open(PATH_RESULT_RS, mode='w') as f:
       for eachTicker in tickerList:
            rawScore = '-' if eachTicker.invalid else eachTicker.RSRawScore()
            f.write(eachTicker.symbol + '\t' + str(eachTicker.RS) + '\t' + str(rawScore) +  '\n')
    
    print('RS一覧を出力>>' + PATH_RESULT_RS)

    
