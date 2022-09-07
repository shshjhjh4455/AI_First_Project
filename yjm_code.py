import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import font_manager, rc
rc('font', family=font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name())


''' 전처리
df1 = pd.read_csv('C:/Users/opqrs/OneDrive/바탕 화면/data1.csv',encoding='cp949',header=None)

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

# 분기 열로 넣기
df1 = df1.reset_index()
df1.insert(0, 'year',  df1.apply(lambda row: row['날짜'].split('/')[0], axis=1))
df1.insert(0, 'month', df1.apply(lambda row: row['날짜'].split('/')[1], axis=1))
df1 = df.set_index('날짜')

df1.to_csv('C:/Users/opqrs/OneDrive/바탕 화면/data.csv',encoding='cp949')
'''

# 
df1 = pd.read_csv("C:/Users/opqrs/OneDrive/문서/GitHub/AI_First_Project/customer_payment_data.csv",encoding='cp949',header=None)
df = df1
df.columns = df.iloc[0,:]
df = df.drop([0],axis=0)
df = df.set_index('날짜')
df = df.astype('float')

# 분기 열로 넣기
df = df.reset_index()
df.insert(0, 'year',  df.apply(lambda row: row['날짜'].split('/')[0], axis=1))
df.insert(0, 'month', df.apply(lambda row: row['날짜'].split('/')[1], axis=1))
df = df.set_index('날짜')
# df = df['2017/07':'2022/05']
'''
# 지역별로 추출
df[df.columns[ pd.Series(df.columns).str.startswith('전국')]]
df = df[df.columns[ pd.Series(df.columns).str.contains('서울')]]
'''

#
df.insert(2,'periods','periods')
df['2017/07':'2019/12'].iloc[:,2] = 'Pre'
df['2020/01':'2022/05'].iloc[:,2] = 'With'
#########################################################################################################################################
'''
df=df.groupby('periods').mean()
df=df[df.columns[ pd.Series(df.columns).str.contains('서울')]]
''' 

'''
df = df.drop('index',axis=1)
df2=df.set_index('periods').T

plt.tight_layout()
df2[1:].plot.bar(rot=90)
'''


''' 상승률 
df2=df.groupby('year').sum()
for i in range(0,12):
    for j in range(0,738):
        df2.iloc[i,j] = df2.iloc[i+1,j]/df2.iloc[i,j]    

df3=df2.shift(1)

df3.to_excel('C:/Users/opqrs/OneDrive/바탕 화면/상승률.xlsx')
'''



### 연령별인구현황

'''
import os
path = "C:/Users/opqrs/Downloads/연령별인구현황"
file_list = os.listdir(path)

c = pd.DataFrame()
for i in range(0,16):
    a = pd.read_csv("C:/Users/opqrs/Downloads/연령별인구현황/201712_202112_연령별인구현황_연간 ("+str(i)+").csv",encoding='cp949')
    b = a.iloc[0,:]
    c = pd.concat([c,b],axis=1)

del a, b
c.to_excel('C:/Users/opqrs/OneDrive/바탕 화면/인구통계.xlsx')
'''

# 인구통계 엑셀로 전처리한 데이터 로드
df = pd.read_csv('C:/Users/opqrs/OneDrive/바탕 화면/population.csv',encoding='cp949')

a = df.groupby(['year','age','gender']).sum()
a = a.reset_index()
a = a.set_index('age')
a = a.drop(['연령구간인구수','총인구수'])
a = a.set_index('gender')
a = a.drop(['계'])
a = a.reset_index()

# sns.color_palette("Paired", 9)
# sns.color_palette("Set3", 10)
# sns.color_palette("bright")
sns.set_palette(sns.color_palette("Set3", 10))

# 연도별 / 지역별 / 연령대 
for i in range(3,18):
    plt.figure(figsize=(15,15))
    sns.barplot(data=a,
                x='age',
                y=a.columns[i],
                hue='year')
    plt.xlabel('Age',fontsize=20)
    plt.xticks(fontsize=20, rotation=45)
    plt.yticks(fontsize=20)
    plt.ylabel(a.columns[i],fontsize=20)
    plt.legend(loc='best',fontsize=20 )
    plt.savefig('C:/Users/opqrs/OneDrive/바탕 화면/'+a.columns[i]+'png')

# 연도별 / 성비
for i in range(3,18):
    plt.figure(figsize=(15,15))
    sns.barplot(data=a,
                x='year',
                y=a.columns[i],
                hue='gender',
                ci=None)
    plt.xlabel('gender',fontsize=20)
    plt.xticks(fontsize=20, rotation=45)
    plt.yticks(fontsize=20)
    plt.ylabel(a.columns[i],fontsize=20)
    plt.legend(loc='best',fontsize=20 )



## 연도별 / 지역별 성비
df = pd.read_csv('C:/Users/opqrs/OneDrive/문서/GitHub/AI_First_Project/population.csv',encoding='cp949')
a = df.groupby(['year','age','gender']).sum()
a = a.reset_index()
a = a.set_index('age')
a = a.drop(['연령구간인구수','총인구수'])
a = a.reset_index()
a = a.set_index('gender')
a = a.drop(['계'])
a = a.reset_index()

## 
year=2021
for i in range(3,19):
    plt.style.use('ggplot')
    plt.figure(figsize=(9,5),dpi=300)
    plt.tight_layout()
    plt.rc('font',family = 'Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.barh(a.loc[(a['gender']=='남') & (a['year']==year) ]['age'],
             -a.loc[(a['gender']=='남') & (a['year']==year) ][a.columns[i]] , label='남성')
    
    plt.barh(a.loc[(a['gender']=='여') & (a['year']==year) ]['age'],
             a.loc[(a['gender']=='여') & (a['year']==year) ][a.columns[i]] , label='여성')
    
    plt.title(str(year)+'년 '+a.columns[i]+'지역 연령별 성비')
    
    # text
    male=pd.concat([a.loc[(a['gender']=='남') & (a['year']==year) ]['age'],
               a.loc[(a['gender']=='남') & (a['year']==year) ][a.columns[i]]
               ],axis=1).reset_index().drop('index',axis=1)

    female=pd.concat([a.loc[(a['gender']=='여') & (a['year']==year) ]['age'],
               a.loc[(a['gender']=='여') & (a['year']==year) ][a.columns[i]]
               ],axis=1).reset_index().drop('index',axis=1)

    plt.text(0,9.8,'('+'{0:,}'.format(male[a.columns[i]][10])+'명) '+str(round(round(male[a.columns[i]][10]/(male[a.columns[i]][10]+female[a.columns[i]][10]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][10]/(male[a.columns[i]][10]+female[a.columns[i]][10]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][10])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,8.8,'('+'{0:,}'.format(male[a.columns[i]][9])+'명) '+str(round(round(male[a.columns[i]][9]/(male[a.columns[i]][9]+female[a.columns[i]][9]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][9]/(male[a.columns[i]][9]+female[a.columns[i]][9]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][9])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,7.8,'('+'{0:,}'.format(male[a.columns[i]][8])+'명) '+str(round(round(male[a.columns[i]][8]/(male[a.columns[i]][8]+female[a.columns[i]][8]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][8]/(male[a.columns[i]][8]+female[a.columns[i]][8]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][8])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,6.8,'('+'{0:,}'.format(male[a.columns[i]][7])+'명) '+str(round(round(male[a.columns[i]][7]/(male[a.columns[i]][7]+female[a.columns[i]][7]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][7]/(male[a.columns[i]][7]+female[a.columns[i]][7]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][7])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,5.8,'('+'{0:,}'.format(male[a.columns[i]][6])+'명) '+str(round(round(male[a.columns[i]][6]/(male[a.columns[i]][6]+female[a.columns[i]][6]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][6]/(male[a.columns[i]][6]+female[a.columns[i]][6]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][6])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,4.8,'('+'{0:,}'.format(male[a.columns[i]][5])+'명) '+str(round(round(male[a.columns[i]][5]/(male[a.columns[i]][5]+female[a.columns[i]][5]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][5]/(male[a.columns[i]][5]+female[a.columns[i]][5]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][5])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,3.8,'('+'{0:,}'.format(male[a.columns[i]][4])+'명) '+str(round(round(male[a.columns[i]][4]/(male[a.columns[i]][4]+female[a.columns[i]][4]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][4]/(male[a.columns[i]][4]+female[a.columns[i]][4]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][4])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,2.8,'('+'{0:,}'.format(male[a.columns[i]][3])+'명) '+str(round(round(male[a.columns[i]][3]/(male[a.columns[i]][3]+female[a.columns[i]][3]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][3]/(male[a.columns[i]][3]+female[a.columns[i]][3]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][3])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,1.8,'('+'{0:,}'.format(male[a.columns[i]][2])+'명) '+str(round(round(male[a.columns[i]][2]/(male[a.columns[i]][2]+female[a.columns[i]][2]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][2]/(male[a.columns[i]][2]+female[a.columns[i]][2]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][2])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,0.8,'('+'{0:,}'.format(male[a.columns[i]][1])+'명) '+str(round(round(male[a.columns[i]][1]/(male[a.columns[i]][1]+female[a.columns[i]][1]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][1]/(male[a.columns[i]][1]+female[a.columns[i]][1]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][1])+'명)'
  ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.text(0,-0.2,'('+'{0:,}'.format(male[a.columns[i]][0])+'명) '+str(round(round(male[a.columns[i]][0]/(male[a.columns[i]][0]+female[a.columns[i]][0]),3)*100,2))+'%' +'  '+ str(round(round(female[a.columns[i]][0]/(male[a.columns[i]][0]+female[a.columns[i]][0]),3)*100,2))+'%'+' ('+'{0:,}'.format(female[a.columns[i]][0])+'명)'
 ,color='black',horizontalalignment='center', fontsize=6)
    
    plt.xticks(color='w')
    plt.tick_params(axis='x',direction='in',length=0)

    
    plt.savefig('C:/Users/opqrs/OneDrive/문서/GitHub/AI_First_Project/지역_연령별_성비/'+str(year)+'년 '+a.columns[i])
###

