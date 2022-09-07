# 전처리
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
