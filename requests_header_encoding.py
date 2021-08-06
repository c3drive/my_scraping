import sys
import requests

# url = sys.argv[1]
url = 'http://gihyo.jp/db'
r = requests.get(url)
print(f'encoding: {r.encoding}, file=sys.stderr')
print(r.text)