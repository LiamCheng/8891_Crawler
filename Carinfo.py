from selenium import webdriver
from bs4 import BeautifulSoup
import re
import string
import pandas as pd

'''
url : 車子網址
brand : 品牌
function get(url , brand) : 輸出csv擋至8891資料夾

'''

def get(url, brand):
    driver = webdriver.Firefox(executable_path='geckodriver.exe')
    driver.get(url)
    pageres = BeautifulSoup(driver.page_source, "lxml")
    # ==========啟動Firefox到傳入的url
    filename = re.sub('[' + string.punctuation + ']', ' ', (pageres.select('.summary-top-name')[1].text))
    filepath = "8891/" + brand + '/' + filename + ".csv"
    carnames = [carname.text for carname in pageres.select('.comp-col-list-nm')]
    carnames.insert(0, 'Name')
    i = 0
    dict = {}
    for carname in carnames:  # 車名
        dict[carname] = list()
    for carinfo in pageres.select('.comp-item'):  # 抓取表格內的資訊
        for dd in carinfo.find_all('dd', id=True):
            dict[carnames[i]].append(dd.text)
        i = i + 1

    driver.close()
    data = pd.DataFrame.from_dict(dict)
    cols = data.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Name')))
    df = data.reindex(columns=cols)
    df.to_csv(filepath, encoding='utf_8_sig', index=False)
    print(pageres.select('.summary-top-name')[1].text.strip(" "), " done")