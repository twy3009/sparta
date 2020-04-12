from selenium import webdriver
from bs4 import BeautifulSoup

import time
import re

import datetime


def GetWeekNumberLastDate(year, weekNumber):
    yearFirstDate = datetime.datetime(year, 1, 1)
    currentDate = yearFirstDate + datetime.timedelta(weeks=weekNumber - 1)
    targetDate = currentDate - datetime.timedelta(days=currentDate.isoweekday() % 7 - 7)
    results = targetDate.strftime('%Y%m%d')
    return results

def GetWeekNumberFirstDate(year, weekNumber):
    yearFirstDate = datetime.datetime(year, 1, 1)
    currentDate = yearFirstDate + datetime.timedelta(weeks=weekNumber - 1)
    targetDate = currentDate - datetime.timedelta(days=currentDate.isoweekday() % 7 - 1)
    results = targetDate.strftime('%Y%m%d')
    return results

# 셀레니움을 실행하는데 필요한 크롬드라이버 파일을 가져옵니다.
driver = webdriver.Chrome('chromedriver')

# 네이버 주식페이지 url을 입력합니다.
name ='삼성전자주가'
print(name)
for i in range(1,52):
    first = GetWeekNumberFirstDate(2019,i)
    Last = GetWeekNumberLastDate(2019, i)
    url = 'https://search.naver.com/search.naver?&where=news&query='+name+'&sm=tab_tmr&frm=mr&nso=so:r,p:from'+first+'to'+Last+',a:all&sort=0'
    #url = 'https://search.naver.com/search.naver?&where=news&query=' + name + '&sm=tab_tmr&frm=mr&nso=so:r,p:from20200411to20200411,a:all&sort=0'
    # 크롬을 통해 네이버 주식페이지에 접속합니다.
    driver.get(url)

    # 정보를 받아오기까지 2초를 잠시 기다립니다.
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    new_count = soup.select_one('#main_pack > div.news.mynews.section._prs_nws > div.section_head > div.title_desc.all_my > span').text.split('/')
    results =re.findall("\d+",new_count[1])
    print(i, new_count[1])
# 크롬에서 HTML 정보를 가져오고 BeautifulSoup을 통해 검색하기 쉽도록 가공합니다.


# 크롬을 종료합니다.
driver.quit()