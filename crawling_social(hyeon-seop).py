from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
import time
import pandas as pd


def crawl_title():
    try:
        title = driver.find_element_by_xpath('//*[@id="section_body"]/ul[{1}]/li[{0}]/dl/dt[2]/a'.format(i, j)).text
        title = re.compile('[^가-힣|a-z|A-Z ]').sub(' ', title)
        print(title)
        titles.append(title)
    except NoSuchElementException:
        title = driver.find_element_by_xpath('//*[@id="section_body"]/ul[{1}]/li[{0}]/dl/dt/a'.format(i, j)).text
        title = re.compile('[^가-힣|a-z|A-Z ]').sub(' ', title)
        print(title)
        titles.append(title)


options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver',
                          options=options)
df_titles = pd.DataFrame()
pages = [131, 131, 131, 101, 131, 77]
# pages = [337, 406, 595, 100, 130, 76]
category = ['Politics', 'Economic', 'Social', 'Culture',
            'World', 'IT']
social_pages = 2
titles = []

for k in range(1, pages[social_pages]):  # 406
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(social_pages, k)
    driver.get(url)
    # time.sleep(0.01)
    for j in range(1, 5):
        for i in range(1, 6):
            try:
                crawl_title()
            except:
                driver.get(url)
                print('StaleElementReferenceException')
                time.sleep(1)
                crawl_title()
    if k % 50 == 0:
        df_section_titles = pd.DataFrame(titles, columns=['title'])
        df_section_titles['category'] = category[social_pages]
        df_section_titles.to_csv('./crawling/news_{}_{}-{}.csv'.format(category[social_pages], k - 49, k))
        titles = []

df_section_titles = pd.DataFrame(titles, columns='Social')
df_section_titles['category'] = category[social_pages]
df_section_titles.to_csv('./crawling/news_{}_remain.csv'.format(category[social_pages]))
#
# df_titles.to_csv('./crawling/naver_news.csv')
# print(len(titles))
driver.close()