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

## MongoDB
1.wikidataからDL
wget https://gihyo.jp/index.html

2.serviceへmongodbをコピー
sudo cp /usr/bin/mongod /etc/init.d/

3.Mongodb起動
```bash
sudo service /usr/bin/mongod status
sudo service /usr/bin/mongod start
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