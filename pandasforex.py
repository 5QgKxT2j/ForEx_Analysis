from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from analyzer import analyzer
import datetime
import pandas as pd

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,1024')
driver = webdriver.Chrome(chrome_options=options)
driver.get('http://www.fxstreet.jp/forex-tools/rate-history-tools/?tf=1h&period=100&pair=usdjpy')
print("サイト名：{0}".format(driver.title))

base = driver.find_element_by_xpath('//div[@class="section-tool section table-s1 table-tool rate-history"]')

try:
    row = []
    for tr in base.find_elements_by_tag_name('tr'):
        row.append([td.text for td in tr.find_elements_by_tag_name('td')])

except Exception as e:
    print("NG")
    print(e)
driver.quit()

df = pd.DataFrame(row).dropna()
df.columns = ['datetime', 'open', 'high', 'low', 'close']

df['datetime'] = pd.to_datetime(df['datetime'].str.split(',').str[1].str.replace(' ','') + df['datetime'].str.split(',').str[2].str.split().str[0], format='%Y年%m月%d日%H:%M') # convert string to datetime

print(df)
