import os
import mymodule

from requests_oauthlib import OAuth1Session

# 認証情報をセット
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

twitter =OAuth1Session(CONSUMER_KEY,
                       client_secret=CONSUMER_SECRET,
                       resource_owner_key=ACCESS_TOKEN,
                       resource_owner_secret=ACCESS_TOKEN_SECRET)

# timeline
#response = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')

#for status in response.json():
#    print('@' + status['user']['screen_name'], status['text'])

# GET followers/list
url = 'https://api.twitter.com/1.1/followers/list.json'
params = {
    'screen_name': 'sy_selene'
}
response = twitter.get(url, params=params)
json = response.json()

# ファイルに保存する場合
mymodule.file_write_json("data/data.json", json)
json = mymodule.file_read_json("data/data.json")

for users in json['users']:
   print(f"{users['name']}(@{users['screen_name']}), {users['description']}")