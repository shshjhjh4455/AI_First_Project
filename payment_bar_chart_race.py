# conda install -c conda-forge ffmpeg 필수
import requests
import csv
import datetime as dt
from tqdm import tqdm
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
import datetime
import warnings
import pandas as pd
import bar_chart_race as bcr
import matplotlib as plt
# 그래프 그릴 때 한글 깨짐 방지 설정
import os
# Mac OS의 경우와 그 외 OS의 경우로 나누어 설정
if os.name == 'posix':
    plt.rc("font", family="AppleGothic")

else:
    plt.rc("font", family="Malgun Gothic")


from IPython.core.display import display, HTML
display(HTML("<style>.container {width:90% !important;}</style>"))

warnings.filterwarnings(action='ignore')
# import pandas_datareader.data as web
# import FinanceDataReader as fdr

# import mpl_finance


csv_data = pd.read_csv('data/customer_payment_data.csv')

# 전국별로 추출
df1 = csv_data[csv_data.columns[pd.Series(
    csv_data.columns).str.startswith('전국')]]

# '날짜' 열 추출
df2 = csv_data[csv_data.columns[pd.Series(
    csv_data.columns).str.startswith('날짜')]]

# '날짜' 열과 '전국' 열 합치기
df = pd.concat([df2, df1], axis=1)

print(df)


# 전국_합계 열 지우기
df = df.drop('전국_합계', axis=1).reset_index(drop=True)
print(df)

# df = df.pivot_table(values = 'confirmed', index = ['날짜'], columns='region')

df['날짜'] = df['날짜'].astype(str)
df['날짜'] = df['날짜'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m"))
print(df)
print(df.dtypes)

# 소비량 수 누적값으로 만들어주기
df.iloc[:, 1:] = df.iloc[:, 1:].cumsum()
print(df.head())

#####df = df.set_index('날짜')
# bar_chart_race()에 전달되는 데이터프레임은 Timestamp형식의 날짜, 행 인덱스로 설정

# to_datetime  datemage 데이트메이지 포맷지정  오브젯 ㅌ

#날짜 안나옴
# bar_chart_race로 시각화하기
bcr.bar_chart_race(df=df.iloc[:, 1:],
                   n_bars=10,
                   sort='desc',
                   title='전국 소비량 변화',
                   period_length=200,
                   filename='전국_소비량.mp4',
                   )
