# 説明
Investor's business dailyが発表しているRelative Strength(らしきもの)を計算するスクリプトです。  
正確にはIBDの発表する値とは一致しませんが、フィルタリングには十分使える精度かと思います。  
計算式等は以下の記事を参照ください。  
http://bullinu.com/2020/07/11/how-to-calc-relativestrength/

# 使い方
- Python 3.8で動作を確認済です
- yfinanceをインポートしてください。
  - pip install yfinance
- tickerList.txtに改行区切りで、計算したい銘柄のティッカーを入力してください。
- main.pyを実行してください。
- resultRS.txtファイルに結果が出力されます。

# 仕組み
- Yahoo financeのAPIを利用しています

# 変更履歴
Ver1.00 初公開
Ver1.01 以下の改善を実施
・東証のデータに対応(末尾に".TをつけてtickerList.txtに記載すれば取得可能。例. 1301.T)
・基準日を実行開始時にコマンドライン上で変更可能に
・データ取得日が休場日の場合に手修正が必要な問題を修正