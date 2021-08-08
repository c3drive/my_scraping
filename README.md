# my_scraping

## Wikipedia
1.wikidataからDL
https://dumps.wikimedia.org/jawiki/

2.DLしたダンプファイルをテキストに変換
```bash
$ python -m wikiextractor.WikiExtractor --no-templates -o articles -b 100M jawiki-20210801-pages-articles-multistream1.xml-p1p114794.bz2
```

3.頻出単語を抜き出す
```bash
$ python word_frequency.py articles
```

# twitter
1.API利用申請
https://developer.twitter.com/

2.APIキーを発行して、.envに追記

3.データフォルダ作成（すでにある場合不要）
```bash
mkdir data
```
2.実行
```bash
$ forego run python rest_api_with_requests_oauthlib.py
```

# youtube
1.アクセスして同意。プロジェクトを作る。
https://console.cloud.google.com/apis/

2.APIキーを発行して、.envに追記

2.Youtube Data APIを有効にする
https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project={プロジェクトID}

3.
```bash
$ forego run python save_youtube_videos.py 
```

## MongoDB
1.起動パスの確認
```bash
ps --no-headers -o comm 1
```
wget https://gihyo.jp/index.html

2.serviceへmongodbをコピー
sudo cp /usr/bin/mongod /etc/init.d/

3.Mongodb起動
```bash
sudo service mongod status
sudo service mongod start
```
※※起動しない

4.index.htmlの内容をMongoDBに保存
```bash
$ python save_mongo.py
```
※※3ができていないので実行不可

## sqlite3
1.登録
```bash
$ python save_sqlite3.py
```
2.DB参照
```bash
$ sqlite3 top_cities.db 'SELECT * FROM cities'
```

## ヒストリー
1.為替データ取得
https://www.stat-search.boj.or.jp/
2.金利情報
https://www.mof.go.jp/jgbs/reference/interest_rate/index.htm
3.有効求人倍率
https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00450222&tstat=000001020327
4.実行
python plot_historical_data.py

# Museums
1. httpサーバ起動
```bash
$ python -m http.server
```
2.ブラウザで実行
http://localhost:8000/museums.html