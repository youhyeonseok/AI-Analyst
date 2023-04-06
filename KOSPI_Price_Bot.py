import FinanceDataReader as fdr
import pandas as pd
from tqdm import tqdm
class price_bot:
    def __init__(self):
        pass
    def run(self):
        stock_info = pd.read_csv("KOSPI200.csv")
        stock_info.loc[len(stock_info)] = [stock_info.columns[0], stock_info.columns[1]]
        stock_info.columns = ["code", "name"]
        # 삼성전자(005930) 전체 (1996-11-05 ~ 현재)
        print(">> stock price data crawling start!")
        for i in tqdm(range(len(stock_info))):
            code = stock_info.iloc[i]["code"]
            name = stock_info.iloc[i]["name"]
            try:
                df = fdr.DataReader(str(code))
            except:
                print(">>Data Crawling False...")
            try:
                df.to_csv("Data/price_data/"+str(name)+".csv")
            except:
                print(">>path error...")
price_bot().run()