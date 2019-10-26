from sklearn.utils import shuffle
import pandas as pd
data = pd.read_excel('origin_file_path', header=0, encoding='utf-8')
print(data.head())
data = shuffle(data)
print(data.head())
data_new =  data.reset_index()
print(data_new.head())
data_new_1000 = data_new.head(1000)
data_new_1000.to_excel('new_file.xlsx')