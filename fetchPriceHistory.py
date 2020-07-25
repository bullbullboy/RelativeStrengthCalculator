import yfinance as yf
import os
import datetime
import dateutil
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

def main():
    # 定数 pyファイルと同じディレクトリを読み書き
    PATH_RESULT         = os.path.dirname(__file__) + '/result.txt'
    PATH_TICKER_LIST    = os.path.dirname(__file__) + '/tickerList.txt' 

    # Tickerリストの読み込み
    with open(PATH_TICKER_LIST) as tickerListFile:
        lines = tickerListFile.read()
    
    # 日時文字列作成
    dateOfToday = toStrFromDatetime(datetime.date.today())
    dateOfReference = ["","","",""]
    dateOfReference[0] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-3))
    dateOfReference[1] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-6))
    dateOfReference[2] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-9))
    dateOfReference[3] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-12))

    # 'a': 追記
    with open(PATH_RESULT, mode='w') as f:

        # 取得日をメモ
        f.write(dateOfToday +'\t' + dateOfReference[0]+'\t' + dateOfReference[1]+'\t' + dateOfReference[2]+'\t' + dateOfReference[3] + '\n')

        for count, line in enumerate(lines.split('\n')):
            resultStr = f'{line}\t{fetchClosePrice(line, dateOfToday)}\t{fetchClosePrice(line, dateOfReference[0])}\t{fetchClosePrice(line, dateOfReference[1])}\t{fetchClosePrice(line, dateOfReference[2])}\t{fetchClosePrice(line, dateOfReference[3])}'
            
            #Debug出力
            print(resultStr)

            #ファイルへの本出力
            f.write(resultStr+'\n')
            f.flush() #バッファにたまって即時出力されない問題の解消

main()