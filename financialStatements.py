import dart_fss as dart
import pandas as pd
import re
class dart_bot:
    api_key='21fddf42c2c82c8c7587e0e74147f05d048da5e4'
    def __init__(self, name) -> None:
        self.name = name
        dart.set_api_key(api_key=self.api_key)

    def run(self):
        corp_list = dart.get_corp_list()
        name = self.name
        try:
            samsung = corp_list.find_by_corp_name(name, exactly=True)[0]
            fs = samsung.extract_fs(bgn_de='19500101')
            fs.save(name+".xlsx")
            data = pd.read_excel("fsdata/"+name+".xlsx", sheet_name="Data_cf", index_col=0)
            col = list(data.columns)
            date = []
            for i in col:
                regex = r'\d{4}\d{2}\d{2}-\d{4}\d{2}\d{2}'
                if bool(re.match(regex, i)):
                    date.append(i)
            col_name = list(data["Unnamed: 2"].iloc[2:])
            clean_data = []
            for i in date:
                value = list(data[i].iloc[2:])
                clean_data.append(value)
            date = [i[:8] for i in date]
            clean_data = pd.DataFrame(clean_data, columns = col_name, index=date)
            clean_data = clean_data.sort_index(ascending=True)
            clean_data.to_csv("Data/Statements_data/"+name+".csv")
        except:
            print("None Data :",name)