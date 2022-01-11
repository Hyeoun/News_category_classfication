from selenium import webdriver
from selenium.common.exceptions import *
import pandas as pd
import re
import time

def crawl_title(a, b):
    try:
        title = driver.find_element_by_xpath(
            '//*[@id="section_body"]/ul[{0}]/li[{1}]/dl/dt[2]/a'.format(a, b)).text  # 이미지가 있는 경우
        title = re.compile('[^가-힣a-zA-Z ]').sub(' ', title)
        titles.append(title)
    except NoSuchElementException:
        title = driver.find_element_by_xpath(
            '//*[@id="section_body"]/ul[{0}]/li[{1}]/dl/dt/a'.format(a, b)).text  # 이미지가 없는 경우
        title = re.compile('[^가-힣a-zA-Z ]').sub(' ', title)
        titles.append(title)

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')  # 가상 컴퓨터에서 실행할때
options.add_argument('--disable-dev-shm-usage')  # 리눅스에서 사용시
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options = options)  # exe 빼야 한다.

df_titles = pd.DataFrame()
pages = [131, 131, 131, 101, 131, 77]
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

for l in range(6):
    titles = []
    for k in range(1, pages[l]):
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{1}#&date=%2000:00:00&page={0}'.format(k, l)
        driver.get(url)
        for j in range(1, 5):
            for i in range(1, 6):
                try:
                    crawl_title(j, i)
                except StaleElementReferenceException:
                    time.sleep(0.2)
                    driver.get(url)
                    print('loading {} page'.format(k))
                    time.sleep(0.5)  # url 검색시 늦어져서 못받아들일 경우 대기시간을 준다.
                    crawl_title(j, i)
                except:
                    print('error')
        if k % 50 == 0:
            df_section_titles = pd.DataFrame(titles, columns=['title'])
            df_section_titles['category'] = category[l]
            df_section_titles.to_csv('./crawling/news_{}_{}-{}.csv'.format(category[l], k-49, k), index=False)

            df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
            titles = []

    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[l]
    df_section_titles.to_csv('./crawling/news_{}_remain.csv'.format(category[l]), index=False)

    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

df_titles.to_csv('./crawling/naver_news.csv', index=False)
driver.close()
print(len(titles))
# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[3]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[3]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[2]/dl/dt/a