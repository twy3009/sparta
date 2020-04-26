from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('mongodb://test:test@15.164.103.10', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta



def scrab(name, page) :
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://search.naver.com/search.naver?&where=news&query='+ str(name)+'&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2020.04.06&de=2020.04.26&docid=&nso=so:r,p:from20200406to20200410,a:all&mynews=0&cluster_rank=153&start={}1&refresh_start=0'.format(str(page-1)),headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    #lis = soup.find_all('li')
    urls = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul>li')
    #print(urls2)
    result = []

    for url in urls :
        test = url.select_one('a')
        test2 = test.attrs['href']
        result.append(test2)

    return result

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.articles.find({},{'_id':0}))
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'articles':result})

@app.route('/table', methods=['GET'])
def listing_table():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.collection.find({},{'_id':0}))

    return jsonify({'result':'success', 'collection':result})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
		# 클라이언트로부터 데이터를 받는 부분
    name = request.form['url_give']
    url_receive = scrab(name,1)[4]
    comment_receive = request.form['comment_give']

		# meta tag를 스크래핑 하는 부분
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

		# mongoDB에 넣는 부분
    article = {'url': url_receive, 'comment': comment_receive, 'image': url_image,
               'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=80,debug=True)