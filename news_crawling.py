import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd

class news_data_bot:
    default_url = "https://search.seoul.co.kr/issueRanking.php"
    def __init__(self, search_word):
        self.search_word = search_word
        
    def run(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.default_url)
        element = driver.find_element(By.CSS_SELECTOR, "#keyword")
        element.send_keys(self.search_word + Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, "#scopeBtn_title").click()
        driver.find_element(By.CSS_SELECTOR, "#sub_option > a").click()

        curr_url = driver.current_url
        curr_url = curr_url + "&pageNum="

        curr = 1
        news_data = []
        while True:
            href = curr_url + str(curr)
            try:
                driver.get(href)
            # 페이지가 없으므로 종료
            except:
                break
            news_list = driver.find_elements(By.CSS_SELECTOR, "#list_area > dl")
            for i in range(len(news_list)):
                text_form = r'\d{4}. \d{2}. \d{2}'
                date, text, href = None, None, None
                if bool(re.match(text_form, news_list[i].find_element(By.CSS_SELECTOR, "#date").text)):
                    date = re.findall(text_form, news_list[i].find_element(By.CSS_SELECTOR, "#date").text)[0].replace(' ', '').replace('.', '-')
                try:
                    href = news_list[i].find_element(By.CSS_SELECTOR, "dt > a").get_attribute("href")
                    main = webdriver.Chrome(ChromeDriverManager().install())
                    main.get(href)
                    time.sleep(1)
                    text = main.find_element(By.CSS_SELECTOR, "#atic_txt1").text
                    main.quit()
                except:
                    pass
                if href == None:
                    href = ""
                if date == None:
                    date = ""
                if text == None:
                    text = ""
                news_data.append([date, text, href])

            curr += 1
        pd.DataFrame(news_data, columns= ["date", "content", "href"]).to_csv("Data/news_data"+self.search_word + ".csv")