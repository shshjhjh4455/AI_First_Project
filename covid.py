from IPython.core.display import display, HTML
display(HTML("<style>.container {width:90% !important;}</style>"))

import warnings
warnings.filterwarnings(action='ignore')
# import pandas_datareader.data as web
# import FinanceDataReader as fdr

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import mpl_finance
import matplotlib.ticker as ticker
from tqdm import tqdm

import csv, requests
import datetime
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

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

covid_df = pd.DataFrame(csv_data, columns = ['date','region','confirmed','death','released'])
covid_df.to_csv('covid19_korea.csv', index=False, header=False, encoding='utf8')

print(covid_df.head())

## 전체지역 확진자수 그룹바이
total_covid_df = covid_df.groupby(['date'])['confirmed'].sum().reset_index(name='counts')

total_covid_df = total_covid_df.rename(columns={'date':'Date'})
total_covid_df['Date'] = total_covid_df['Date'].astype(str)

print(total_covid_df.head())

## Date 데이터타입 변경
total_covid_df['Date'] = total_covid_df['Date'].apply(lambda x: datetime.datetime.strptime(x,"%Y%m%d")) 

print(total_covid_df.head())

csv_data = pd.read_csv(
    '/Users/bagjeonghyeon/Downloads/price_total.csv', header=None)

# 행 열 설정
csv_data.columns = ['Date', 'Price']
csv_data['Date'] = csv_data['Date'].astype(str)
# chage . to -
#csv_data['Date'] = csv_data['Date'].str.replace('.', '-')
total_covid_df['Date'] = total_covid_df['Date'].astype(str)
print (csv_data.head())


price_covid = pd.merge(csv_data, total_covid_df, on='Date').reset_index(drop=True)
price_covid['datatime'] = price_covid['Date'].apply(lambda x: datetime.datetime.strptime(x,"%Y%m%d"))
price_covid['Price'] = price_covid['Price'].astype(int)

# make plot using price_covid 
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

# x 축에 datetime, y 축에 Price
ax.plot(price_covid['datatime'], price_covid['Price'], label='Price')

# 그래프 그리기


    


