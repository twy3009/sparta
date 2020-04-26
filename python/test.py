import pandas as pd

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('mongod://test:test@15.164.103.10', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
code_df = code_df[['회사명', '종목코드']]
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
#print(code_df.head())


def get_url(item_name, code_df):
    code =code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    # print(code)
    url = 'http://finance.naver.com/item/sise_day.nhn?code='+code.strip()
    # print("요청 URL = {}".format(url))
    return url

item_name='삼성전자'
url = get_url(item_name, code_df)
# print(url)
df = pd.DataFrame()

for page in range(1, 21):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

df = df.dropna()


db.collection.insert_many(df.to_dict('records'))







