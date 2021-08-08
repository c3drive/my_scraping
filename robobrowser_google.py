from robobrowser import RoboBrowser

# Robobrowser オブジェクトを作成する
browser = RoboBrowser(parser='html.parser')

# Google のトップページを開く
browser.open('https://www.google.co.jp/')

# 検索語を入力して送信する
form = browser.get_form(action='/search')
form['q'] = 'Python'
# Google 検索ボタンを押す
browser.submit_form(form, list(form.submit_fields.values())[0])
# 検索結果のタイトルと URL を抽出して表示
for a in browser.select('h3 > a'):
    print(a.text)
    print(a.get('href'))