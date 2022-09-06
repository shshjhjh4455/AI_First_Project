import requests
import csv
import seaborn as sns
import datetime as dt
from tqdm import tqdm
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import warnings
from IPython.core.display import display, HTML
display(HTML("<style>.container {width:90% !important;}</style>"))

warnings.filterwarnings(action='ignore')
#import pandas_datareader.data as web
# import FinanceDataReader as fdr

# import mpl_finance


CSV_URL = 'https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_regional_daily.csv'

# 확진, 사망, 격리해제
yesterday_data = {}
yesterday_data['서울'] = [0, 0, 0]
yesterday_data['부산'] = [0, 0, 0]
yesterday_data['대구'] = [0, 0, 0]
yesterday_data['인천'] = [0, 0, 0]
yesterday_data['광주'] = [0, 0, 0]
yesterday_data['대전'] = [0, 0, 0]
yesterday_data['울산'] = [0, 0, 0]
yesterday_data['세종'] = [0, 0, 0]
yesterday_data['경기'] = [0, 0, 0]
yesterday_data['강원'] = [0, 0, 0]
yesterday_data['충북'] = [0, 0, 0]
yesterday_data['충남'] = [0, 0, 0]
yesterday_data['전북'] = [0, 0, 0]
yesterday_data['전남'] = [0, 0, 0]
yesterday_data['경북'] = [0, 0, 0]
yesterday_data['경남'] = [0, 0, 0]
yesterday_data['제주'] = [0, 0, 0]
yesterday_data['검역'] = [0, 0, 0]

flag = False
csv_data = []

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        if row[0] == 'date':
            continue

        # 다음부터 과거 데이터의 차이만 다시 저장한다.
        row[2] = int(row[2]) - int(yesterday_data[row[1]][0])
        row[3] = int(row[3]) - int(yesterday_data[row[1]][1])
        row[4] = int(row[4]) - int(yesterday_data[row[1]][2])

        # 누적 데이터 저장
        yesterday_data[row[1]][0] += row[2]
        yesterday_data[row[1]][1] += row[3]
        yesterday_data[row[1]][2] += row[4]

        csv_data.append(row)

covid_df = pd.DataFrame(
    csv_data, columns=['date', 'region', 'confirmed', 'death', 'released'])
covid_df.to_csv('covid19_korea.csv', index=False,
                header=False, encoding='utf8')

print(covid_df.head())

# 전체지역 확진자수 그룹바이
total_covid_df = covid_df.groupby(
    ['date'])['confirmed'].sum().reset_index(name='counts')

total_covid_df = total_covid_df.rename(columns={'date': 'Date'})
total_covid_df['Date'] = total_covid_df['Date'].astype(str)

print(total_covid_df.head())

# Date 데이터타입 변경
total_covid_df['Date'] = total_covid_df['Date'].apply(
    lambda x: datetime.datetime.strptime(x, "%Y%m%d"))

print(total_covid_df.head())

# 일간 데이터 월간 데이터로 변환
total_covid_df = total_covid_df.groupby(
    total_covid_df['Date'].dt.strftime('%Y-%m')).sum()
print(total_covid_df.head())

csv_data = pd.read_csv(
    '/Users/bagjeonghyeon/Downloads/price_total.csv', header=None)


# 행 열 설정
csv_data.columns = ['Date', 'Price']
csv_data['Date'] = csv_data['Date'].astype(str)
# chage . to -
#csv_data['Date'] = csv_data['Date'].str.replace('.', '-')
#total_covid_df['Date'] = total_covid_df['Date'].astype(str)
print(csv_data.head())


price_covid = pd.merge(csv_data, total_covid_df,
                       on='Date').reset_index(drop=True)
price_covid['datetime'] = price_covid['Date'].apply(
    lambda x: datetime.datetime.strptime(x, "%Y-%m"))
price_covid['Price'] = price_covid['Price'].astype(int)

print(price_covid.head())


# datetime 열 버리기
# price_covid = price_covid.drop('datetime', axis=1)
# print(price_covid)

# csv 파일로 저장
price_covid.to_csv('price_covid.csv')

# 전체기간 확진자와 소비량 상관관계 분석
print(price_covid.corr())

# 2020 확진자와 소비량 상관관계 분석
price_covid_corr_df = price_covid[price_covid.datetime.dt.year == 2020].reset_index(
)
price_covid_corr_df.drop('index', axis=1, inplace=True)
print(price_covid_corr_df.corr())

# 2021 확진자와 소비량 상관관계 분석
price_covid_corr_df = price_covid[price_covid.datetime.dt.year == 2021].reset_index(
)
price_covid_corr_df.drop('index', axis=1, inplace=True)
print(price_covid_corr_df.corr())

# 2022 확진자와 소비량 상관관계 분석
price_covid_corr_df = price_covid[price_covid.datetime.dt.year == 2022].reset_index(
)
price_covid_corr_df.drop('index', axis=1, inplace=True)
print(price_covid_corr_df.corr())
