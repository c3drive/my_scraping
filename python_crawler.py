# reモジュールをインポートする
import re
# timeモジュールをインポートする
import time

import requests
import lxml.html

from pymongo import MongoClient

def main():
    """
    クローラーのメインの処理
    """
    # ローカルホストのMongoDBに接続する
    client = MongoClient('localhost', 27017)
    # scrapingデータベースのebooksコレクションを得る
    #collection = client.scraping.ebooks
    # データを一位に識別するキーを格納するkeyフィールドにユニークなインデックスを作成する
    #collection.create_index('key', unique=True)

    #複数のページをクロールするのでSessionを使う
    session = requests.Session()

    response = requests.get('https://gihyo.jp/dp')
    # scrape_list_page()関数を呼び出し、ジェネレーターイテレーターを取得する
    urls = scrape_list_page(response)
    for url in urls:
        # urlからキーを取得する
        #key = extract_key(url)

        #MongoDBからキーに該当するデータを探す
        #ebook = collection.find_one({'key': key})
        ebook = False
        #MongoDBに存在しない場合だけ、詳細ページをクロールする
        if not ebook:
            # 1秒のウェイトを入れる
            time.sleep(1)
            # Sessionを使って詳細ページを取得する
            response = session.get(url)
            # 詳細ページからスクレイピングして電子書籍の情報を得る
            ebook = scrape_detail_page(response)
            # 電子書籍の情報をMongoDBに保存する
            #collection.insert_one(ebook)

        # 電子書籍の情報を表示する
        print(ebook)


def scrape_list_page(response: requests.Response):
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数
    """
    html = lxml.html.fromstring(response.text)
    # 絶対URLに変換する
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        # yield文でジェネレーターイテレーターの要素を返す
        yield url

def scrape_detail_page(response: requests.Response) -> dict:
    """
    詳細ページのResponseから電子書籍の情報をdictで取得する
    """
    html = lxml.html.fromstring(response.text)
    ebook = {
        # url
        'url': response.url,
        # タイトル
        'title': html.cssselect('#bookTitle')[0].text_content(),
        # 価格（.textで直接の子である文字列のみを取得）, strip()で前後の空白を削除
        'price': html.cssselect('.buy')[0].text.strip(),
        # 目次
        'content': [normalize_spaces(h3.text_content()) for h3 in html.cssselect('#content > h3')]
    }
    # dictを返す
    return ebook

def extract_key(url: str) -> str:
    """
    URLからキー（URLの末尾のISBN）を抜き出す
    """
    # 最後の/から文字列末尾までを正規表現で取得
    m = re.search(r'/([^/]+)$', url)
    return m.group(1)

def normalize_spaces(s: str) -> str:
    """
    連続する空白を１つのスペースに置き換え、前後の空白を削除した新しい文字列を取得する
    """
    return re.sub(r'\s+', ' ', s).strip()


if __name__ == '__main__':
    main()