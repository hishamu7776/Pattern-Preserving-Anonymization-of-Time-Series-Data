import os
import random

import numpy as np
import pandas as pd
import utility as Utility
import top_down as TopDown

path = 'dataset/Sales_Transactions_Dataset_Weekly.csv'
Utility.clean_data(path=path,final_column='W51')
dataset = pd.read_csv("dataset/Sales_Transactions_Dataset_Weekly_Cleaned.csv")
QI_names = dataset.columns[1:]
id_col = dataset.columns[0]
min_attr,max_attr = Utility.get_min_max_attributes(dataset)
data_dict = dict()
for idx, row in dataset.iterrows():
  data_dict[row[id_col]] = list(row[QI_names])
duplicate = data_dict.copy()
k_anonymized_data = list()
TopDown.topdown_greedy(data=duplicate, k_val=5, max_val=max_attr, min_val=min_attr, k_anonymized=k_anonymized_data,columns=QI_names)