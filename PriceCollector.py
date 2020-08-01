import yfinance as yf
import datetime
import dateutil
import Common

from dateutil.relativedelta import relativedelta

def fetchClosePrice(ticker, date):
    try:
        ticker=yf.Ticker(ticker)
        return ticker.history(start=date, end=date).Close.values[0]
    except:
        return "-"

def toStrFromDatetime(datetime):
    # https://qiita.com/xza/items/9618e25a8cb08c44cdb0
    return f'{datetime:%Y-%m-%d}'

def collectPrice():
    # 定数 pyファイルと同じディレクトリを読み書き
    PATH_RESULT         = Common.pathOfPriceResult()
    PATH_TICKER_LIST    = Common.pathOfTickerList()

    # Tickerリストの読み込み
    with open(PATH_TICKER_LIST) as tickerListFile:
        lines = tickerListFile.read()
    
    # 日時文字列作成
    dateOfToday = toStrFromDatetime(datetime.date.today())
    dateOfReference = ["","","",""]

    # TODO [bugfix]実行日によってはデータ取得ができない問題あり。現状は手動で日にちをずらす必要がある。
    # 例) dateOfReference[0] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-3, days=-1))
    dateOfReference[0] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-3))
    dateOfReference[1] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-6))
    dateOfReference[2] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-9))
    dateOfReference[3] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-12))

    # 'a': 追記
    with open(PATH_RESULT, mode='w') as f:

        # ヘッダー出力
        f.write("ticker\t" + dateOfToday +'\t' + dateOfReference[0]+'\t' + dateOfReference[1]+'\t' + dateOfReference[2]+'\t' + dateOfReference[3] + '\n')

        # 価格出力
        splittedLines = lines.split('\n')
        for count, line in enumerate(splittedLines):
            resultStr = f'{line}\t{fetchClosePrice(line, dateOfToday)}\t{fetchClosePrice(line, dateOfReference[0])}\t{fetchClosePrice(line, dateOfReference[1])}\t{fetchClosePrice(line, dateOfReference[2])}\t{fetchClosePrice(line, dateOfReference[3])}'
            
            #Debug出力
            print(str(count) + '/' + str(len(splittedLines)) + '\t:' + resultStr)

            #ファイルへの本出力
            f.write(resultStr+'\n')
            f.flush() #バッファにたまって即時出力されない問題の解消
