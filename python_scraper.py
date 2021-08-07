import csv
import re
import sqlite3
from typing import List
import requests
import lxml.html

def main():
    """
    メインの処理。fetch(), scrape(), save()の３つの関数を呼び出す。
    """
    url = 'https://gihyo.jp/dp'
    html = fetch(url)
    books = scrape(html, url)
    save('books.db', books)
    save_file('books.csv', books)

def fetch(url: str)-> str:
    """
    引数urlで与えられたURLのWebページを取得する。
    WebページのエンコーディングはConetnt-Typeヘッダーから取得する。
    戻り値：str型のHTML
    """
    r = requests.get(url)
    return r.text  #HTTPヘッダーから取得したエンコーディングでデコードした文字列を返す

def scrape(html: str, base_url: str)-> List[dict]:
    """
    引数htmlで与えらえたHTMLから正規表現で書籍の情報を抜き出す。
    引数base_urlは絶対URLに変換する際の基準となるURLを指定する。
    戻り値：書籍（dict）のリスト
    """
    books =[]
    html = lxml.html.fromstring(html)
    html.make_links_absolute(base_url)  #すべてのa要素のhref属性を絶対URLに変換する。

    #cssselect()メソッドで、セレクターに該当するa要素のリストを取得して、ここのa要素に対して処理を行う。
    #セレクターの意味：id="listBook"である要素　の直接の子であるli要素 の直接の子であるitemprop="url"という属性を持つa要素
    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        #a要素のhref属性から書籍のurlを取得する。
        url = a.get('href')

        #書籍のタイトルはitemprop="name"という属性を持つp要素から取得する。
        p = a.cssselect('p[itemprop="name"]')[0]
        title = p.text_content()  #wbr要素などが含まれているのでtextではなくtext_contentを使う

        books.append({'url':url, 'title':title})

    return books

def save(db_path: str, books: List[dict]):
    """
    引数booksで与えたれた書籍のリストをSQLiteデータベースに保存する。
    データベースのパスは引数db_pathで与えられる。
    戻り値：無し
    """

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS books')
    c.execute('''
        CREATE TABLE books(
            title text,
            url text
        )
    ''')
    c.executemany('INSERT INTO books VALUES(:title, :url)', books)

    conn.commit()
    conn.close()

def save_file(file_path: str, books: List[dict]):
    """
    引数booksで与えたれた書籍のリストをCSV形式のファイルに保存する。
    ファイルのパスは引数file_pathで与えられる。
    戻り値：無し
    """
    with open(file_path, 'w', newline='') as f:
        #第１引数にファイルオブジェクトを、第2引数にフィールド名のリストを指定する。
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader()  #1行目のヘッダーを出力する
        #writerows()で複数の行を１度に出力する。引数は辞書のリスト。
        writer.writerows(books)

#pythonコマンドで実行された場合にmain()関数を呼び出す。これはモジュールとして他のファイルから
#インポートされたときに、mail()関数が実行されないようにするための、pythonにおける一般的なイディオム。
if __name__ == '__main__':
    main()