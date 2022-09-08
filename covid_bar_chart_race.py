 #conda install -c conda-forge ffmpeg 필수
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

corona_csv = pd.DataFrame(csv_data, columns = ['date','region','confirmed','death','released'])
corona_csv.to_csv('covid19_korea_race.csv', index=False, header=False, encoding='utf8')

# print(corona_csv.head())

 

#필요한 데이터만 남기고 지우기
corona = corona_csv[['date','confirmed','region']] # 등록일시분초, 확진자 수, 시도명(영어)

#열 순서 바꾸기 (등록일시, 시도명, 확진자 수 순)
corona = corona[['date','region','confirmed']]

# 검역 열 지우기
corona.drop(corona[corona['region'] == '검역'].index, inplace=True)

# 열값을 지역으로, 값을 확진자 수로 하여 피봇팅하기
corona_df = corona.pivot_table(values = 'confirmed', index = ['date'], columns='region')

# 확진자 수 누적값으로 만들어주기
corona_df.iloc[:,0:-1] = corona_df.iloc[:,0:-1].cumsum()
print(corona_df.head())

#bar_chart_race로 시각화하기
bcr.bar_chart_race(df = corona_df,
                    n_bars= 17,
                    sort='desc',
                    title='Corona in Korea',
                    period_length=30,
                    filename='한국_코로나확진자.mp4',
                    )


