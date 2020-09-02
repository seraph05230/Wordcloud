"""

@author: seraph05230
@url:https://github.com/seraph05230

"""

from selenium import webdriver
from bs4 import BeautifulSoup as soup
from time import sleep
import pandas as pd
from func import Wordcloud as WC

url = 'https://trends.google.com.tw/trends/trendingsearches/daily?geo=TW'

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--incognito')
driver = webdriver.Chrome('./chromedriver', chrome_options = option)
driver.get(url)
driver.implicitly_wait(5)

while True:
    searchDate = input('需要往回蒐集幾天:')
    if searchDate.isnumeric() and int(searchDate) >= 0:
        break

for i in range(int(searchDate)):
    if i == 0:
        print('資料載入中', end = '')
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]').click()
    print('.', end = '')
    sleep(2)

root = soup(driver.page_source, 'lxml')

driver.quit()

datas = root.find_all('div', class_ = 'feed-list-wrapper')
dates = [data.find('div', class_ = 'content-header-title')
         for data in datas]

titles = [title.find_all('a', attrs = {'ng-attr-title':'{{::titlePart.hoverMessage}}'})
         for title in datas]

searchCounts = [data.find_all('div', class_ = 'search-count-title')
         for data in datas]

s_titles = []
s_searchCounts = []

with open('{}~{}.txt'.format(dates[0].string, dates[-1].string), 'w',
          encoding = 'utf-8') as fileAll: #不分日期
    for date, ts, scs in zip(dates, titles, searchCounts):
        #file = open('{}.txt'.format(date.string), 'w', encoding = 'utf-8') #依日期分檔
        for t, sc in zip(ts, scs):
            s_titles += [t.string.strip()]
            s_searchCounts += [sc.string.replace('+', '').replace('萬', '0000')]
            fileAll.write(''.join([t.string.strip(), ',', sc.string.replace('+', '').
                                   replace('萬', '0000'), '\n'])) #不分日期
            #file.write(''.join([t.string.strip(), ',', sc.string.replace('+', '').
                                #replace('萬', '0000'), '\n'])) #依日期分檔

df_ts = pd.DataFrame({'keyword':s_titles, 'searchCount':s_searchCounts})

print('\n資料量:', df_ts.shape[0])

while True:
    nlarge = input('需要取前幾高(1~{}):'.format(df_ts.shape[0]))
    if nlarge.isnumeric() and int(nlarge) > 0:
        break

df_ts['searchCount'] = df_ts['searchCount'].astype(int).nlargest(int(nlarge))

condition = pd.isnull(df_ts['searchCount']) == False
df_ts = df_ts[condition]
df_ts = df_ts.sort_values('searchCount', ascending = False)

df_ts['keyword'].to_csv('Top {} keyword.txt'.format(nlarge), index = False,
                        header = False)

WC.Wordcloud(nlarge)