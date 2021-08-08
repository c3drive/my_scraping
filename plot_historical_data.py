from datetime import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import japanize_matplotlib # 日本語化

matplotlib.use('Agg') 
matplotlib.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']


def main():
    # 為替データ読み込み
    df_exchange = pd.read_csv(
        'data/exchange.csv', encoding='cp932', header=1, 
        names=['date', 'USD', 'rate'], skipinitialspace=True, index_col=0, parse_dates=True)
    # years = {}
    # output = []
    # for index in df_exchange.index:
    #     year = int(index.split('-')[0])
    #     if (year not in years) and (1981 < year < 2014):
    #         if df_exchange.DEXKOUS[index] != ".":
    #             years[year] = True
    #             output.append([year, float(df_exchange.DEXKOUS[index])])
    # df_exchange = pd.DataFrame(output)

    # 国債金利データの読み込み
    df_jgbcm = pd.read_csv(
        'data/jgbcm_all.csv', encoding='cp932', header=1, index_col=0, parse_dates=True, 
        date_parser=parse_japanese_date, na_values=['-'])

    # 有効求人データの読み込み
    df_jobs = pd.read_excel(
        'data/第3表.xlsx', skiprows=3, skipfooter=3, usecols='A, U:AF', index_col=0
        ) 
    s_jobs = df_jobs.stack()
    #print(s_jobs)
    s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]

    min_date = date2num(datetime(1973, 1, 1)) # X軸の最小値
    max_date = date2num(datetime.now()) # X軸の最大値

    # 1つめのサブプロット（国債金利データ）
    plt.subplot(3, 1, 1)    # 3行1列の1番目
    plt.plot(df_exchange.index, df_exchange.USD, label='ドル/円') 
    plt.xlim(min_date, max_date)  # X軸の範囲
    #plt.ylim(50, 250) # y軸の範囲
    plt.legend(loc='best') # 判例を適当な位置に

    # 2つめのサブプロット（為替データ）
    plt.subplot(3, 1, 2)    # 3行1列の2番目
    plt.plot(df_jgbcm.index, df_jgbcm['1年'], label='1年目国債金利') 
    plt.plot(df_jgbcm.index, df_jgbcm['5年'], label='5年目国債金利') 
    plt.plot(df_jgbcm.index, df_jgbcm['10年'], label='10年目国債金利') 
    plt.xlim(min_date, max_date) 
    plt.legend(loc='best')
    
    # 3つめのサブプロット（有効求人倍率）
    plt.subplot(3, 1, 3)    # 3行1列の3番目
    plt.plot(s_jobs.index, s_jobs, label='有効求人倍率（季節調整値）') 
    plt.xlim(min_date, max_date) 
    plt.ylim(0.0, 2.0)
    plt.axhline(y=1, color='gray') # 水平線
    plt.legend(loc='best')

    plt.savefig('historical_data.png', dpi=300) # 画像を保存


def parse_japanese_date(s):
    """
    和暦の日付を立て値目オブジェクトに変換する
    """
    base_years = {'S': 1925, 'H': 1988, 'R': 2019}
    era = s[0]
    year, month, day = s[1:].split('.')
    year = base_years[era] + int(year)
    return datetime(year, int(month), int(day))


def parse_year_and_month(year, month):
    """
    ('X年', 'Y月')の組みをdatetimeオブジェクトに変換する
    """
    year = int(year[:-1]) # 年を除外
    month = int(month[:-3])
    #year += (1900 if year >= 63 else 2000) # 63年以降は19XX, 63より前は20XX
    return datetime(year, month, 1)



if __name__ == '__main__': 
    main()