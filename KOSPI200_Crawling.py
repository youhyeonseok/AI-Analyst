from bs4 import BeautifulSoup
import csv
import os
import re
import requests

BaseUrl = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='

for i in range(1, 21):
    url = BaseUrl + str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    items = soup.find_all('td', {'class': 'ctg'})

    for item in items:
        #print(item)
        txt = item.a.get('href') # https://finance.naver.com/item/main.nhn?code=006390
        k = re.search('[\d]+', txt) ##정규표현식 사용. [\d] 숫자표현, + : 반복
        if k:
            code = k.group()
            name = item.text
            data = code, name

            with open ('KOSPI200.csv', 'a', newline='') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
                writer = csv.writer(f)
                writer.writerow(data)