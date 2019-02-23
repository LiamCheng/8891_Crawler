from bs4 import BeautifulSoup
import requests
import os
from Carinfo import get

'''
filepath = 輸出檔案的位置

'''
if __name__ == '__main__':

    filepath = '8891/'

    res = requests.get('https://c.8891.com.tw/Models', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                                                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                                                                              ' Chrome/45.0.2454.101 Safari/537.36'})
    soup = BeautifulSoup(res.text, 'lxml')
    for brands in soup.select('.gl-i'):
        text = brands.text.strip(" \t\n\r()")
        carnum = text.split("(")[1]
        brand = text.split("(")[0].split('/')[0]
        urlhref = ''.join([a['href'] for a in brands.find_all('a', href=True) if a.text])
        if not os.path.exists(filepath + brand):
            os.makedirs(filepath + brand)
        for carcount in range(1, int(carnum), 24):
            brandurl = 'https://c.8891.com.tw' + urlhref + '?page=' + str(int((carcount / 24) + 1))
            brandres = requests.get(brandurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                     'Chrome/45.0.2454.101 Safari/537.36'})
            brandres = BeautifulSoup(brandres.text, 'lxml')
            for cars in brandres.select('.brand-list-main'):
                car_urls = [a['href'] for a in cars.find_all('a', {"class": "brand-list-img"}, href=True) if
                            a.text]  # 取得品牌頁面的所有車子網址
                for car_url in car_urls:
                    car_url = car_url.replace("Summary", "Specification")  # 轉換規格配備的網頁
                    get(car_url, brand)
