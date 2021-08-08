import os
import sys
from apiclient.discovery import build  # pip install google-api-python-client
from pymongo import MongoClient, DESCENDING

# 環境変数からAPIキーを取得する
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']

def main():
    """
    メイン処理
    """
    #mongo_client = MongoClient('localhost', 27017)
    #collection = mongo_client.youtube.videos
    #collection.delete_many({})

    for items_per_page in search_videos('投資'):
        #     for item in search_response['items']:
        # # 動画のタイトルを表示する
        print(items_per_page)
    #    save_to_mongodb(collection, items_per_page)

    #show_top_videos(collection)

def search_videos(query, max_pages=5):
    """
    動画を検索してページ単位でlistをyieldする
    """
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_request = youtube.search().list(
        part='id',
        q=query,
        type='video',
        maxResults=50,
    )

    i=0
    while search_request and i < max_pages:
        search_response = search_request.execute()
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        # 詳細
        videos_response = youtube.videos().list(
            part='snippet, statistics',
            id=','.join(video_ids)
        ).execute()

        yield videos_response['items']

        # 次のリクエスト
        search_request = youtube.search().list_next(search_request, search_response)


def save_to_mongodb(collection, items):
    """
    MongoDBにアイテムのリストを保存する
    """
    for item in items:
        item['_id'] == item['id']

        for key, value in item['statistics'].items():
            item['statistict'][key] = int(value)
    
    result = collection.insert_many(items)
    print('Inserted {0} documents', format(len(result.inserted_ids)), file=sys.stderr)

def show_top_videos(collection):
    """
    mongoDBコレクション内でビュー数の上位5件を表示する
    """
    for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
        print(item['statistics']['viewCount'], item['snippet']['title'])


if __name__ == '__main__':
    main()