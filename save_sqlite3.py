import sqlite3

conn = sqlite3 .connect('data/top_cities.db') # top_cities.dbファイルを開きコネクション取得

c = conn.cursor()
c.execute('DROP TABLE IF EXISTS cities')
c.execute('''
    CREATE TABLE cities(
        rank integer,
        city text,
        population integer
    )
''')

c.execute('INSERT INTO cities VALUES(?, ?, ?)', (1, '上海', 24150000))

# 辞書
c.execute('INSERT INTO cities VALUES(:rank, :city, :population)',
     {'rank': 2, 'city': 'カラチ', 'population': 23500000})

# 複数
c.executemany('INSERT INTO cities VALUES(:rank, :city, :population)', [
     {'rank': 3, 'city': 'カラチ', 'population': 21516000},
     {'rank': 4, 'city': 'カラチ', 'population': 14722100},
     {'rank': 5, 'city': 'カラチ', 'population': 14160467},
])

conn.commit()

c.execute('SELECT * FROM cities')
for row in c.fetchall():
    print(row)

conn.close