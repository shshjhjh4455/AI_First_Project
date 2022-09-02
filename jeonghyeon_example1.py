import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
import os

df1 = pd.read_csv('/Users/bagjeonghyeon/AI_First_Project/AI_First_Project/data/customer_payment_data.csv',header=None)

df1.columns = df1.iloc[0,:]
df1 = df1.drop([0],axis=0)
df1 = df1.set_index('날짜')
df1 = df1.astype('float')


# 소비유형 공백제거 
df1.iloc[1,:] = [df1.iloc[1,:][i].replace(" ","") for i in range(len(df1.columns))]

# 지역, 소비유형코드 병합
df1.iloc[0,:]=df1.iloc[0,:]+'_'+df1.iloc[1,:]
df1=df1.drop([1],axis=0)

# set col
df1.columns = df1.iloc[0,:]
df1=df1.drop([0],axis=0)


# 날짜변수 외부지표와 통일
df1['지역코드_소비유형코드']=pd.to_datetime(df1['지역코드_소비유형코드'],format="%Y/%m")
df1.insert(0, '날짜', df1['지역코드_소비유형코드'].apply(lambda _: datetime.strftime(_,"%Y/%m")))

# 분기 열로 넣기
df1 = df1.drop(['지역코드_소비유형코드'],axis=1) # 변환 후 날짜 삭제

# set index
df1=df1.set_index('날짜')

df1.to_csv('data.csv',encoding='cp949')

