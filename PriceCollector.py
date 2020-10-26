import yfinance as yf
import datetime
import dateutil
import Common
import os

from dateutil.relativedelta import relativedelta

def fetchClosePrice(ticker, date):
    try:
        ticker=yf.Ticker(ticker)
        dateStartStr=toStrFromDatetime(date)
        dateEndStr=toStrFromDatetime(date + relativedelta(days=+1))
        return ticker.history(start=dateStartStr, end=dateEndStr).Close.values[0]
    except:
        return "-"

def toStrFromDatetime(datetime):
    # https://qiita.com/xza/items/9618e25a8cb08c44cdb0
    return f'{datetime:%Y-%m-%d}'

def toTimeStampStr(datetime0, datetime1, datetime2, datetime3, datetime4):
    return "ticker\t" + toStrFromDatetime(datetime0) +'\t' + toStrFromDatetime(datetime1)+'\t' + toStrFromDatetime(datetime2) + '\t'+ toStrFromDatetime(datetime3)+'\t'+ toStrFromDatetime(datetime4) + '\n'

def collectPrice():
    # 定数 pyファイルと同じディレクトリを読み書き
    PATH_RESULT         = Common.pathOfPriceResult()
    PATH_TICKER_LIST    = Common.pathOfTickerList()

    # 基準日の確認 & 更新
    print("RS計算を行います")
    targetDatetime = datetime.date.today()
    print("基準の日は" + toStrFromDatetime(targetDatetime) + "でよいですか？ y/n")
    inputStr = input()
    if inputStr != "y":
        print("基準とする日を入力してEnterを入力してください。 入力例)" + toStrFromDatetime(targetDatetime))
        inputTargetStr=input()

        try:
            targetDatetime = datetime.datetime.strptime(inputTargetStr, '%Y-%m-%d')
        except:
            print("不正な入力のため処理を中断します")
            return

    print(toStrFromDatetime(targetDatetime) + "を基準日として計算を開始します")

    # Tickerリストの読み込み
    with open(PATH_TICKER_LIST) as tickerListFile:
        lines = tickerListFile.read()
    
    # 日時文字列作成
    dateOfToday = targetDatetime
    dateOfReference = ["","","",""]

    # TODO [bugfix]実行日によってはデータ取得ができない問題あり。現状は手動で日にちをずらす必要がある。
    # 例) dateOfReference[0] = toStrFromDatetime(datetime.date.today() + relativedelta(months=-3, days=-1))
    dateOfReference[0] = dateOfToday + relativedelta(months=-3)
    dateOfReference[1] = dateOfToday + relativedelta(months=-6)
    dateOfReference[2] = dateOfToday + relativedelta(months=-9)
    dateOfReference[3] = dateOfToday + relativedelta(months=-12)

    # Resultフォルダ作成
    resultPath = Common.pathOfResultDir()
    if not os.path.exists(resultPath):
        os.mkdir(Common.pathOfResultDir())

    # 'a': 追記
    with open(PATH_RESULT, mode='w') as f:

        # ヘッダー出力
        header=toTimeStampStr(dateOfToday, dateOfReference[0],dateOfReference[1],dateOfReference[2],dateOfReference[3])
        f.write(header)
        print(header)

        # 価格出力
        splittedLines = lines.split('\n')
        for count, line in enumerate(splittedLines):
            resultStr = f'{line}\t{fetchClosePrice(line, dateOfToday)}\t{fetchClosePrice(line, dateOfReference[0])}\t{fetchClosePrice(line, dateOfReference[1])}\t{fetchClosePrice(line, dateOfReference[2])}\t{fetchClosePrice(line, dateOfReference[3])}'
            
            #Debug出力
            print(str(count) + '/' + str(len(splittedLines)) + '\t:' + resultStr)

            #ファイルへの本出力
            f.write(resultStr+'\n')
            f.flush() #バッファにたまって即時出力されない問題の解消
    
    print('価格一覧を出力>>' + PATH_RESULT)
