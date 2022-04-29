import os
import random

import numpy as np
import pandas as pd
import utility as Utility
import top_down as TopDown
from node import Node

path = 'dataset/Sales_Transactions_Dataset_Weekly.csv'
dataset = pd.read_csv(path)
dataset.dropna(axis=0,inplace=True)
columns = list(dataset.columns)
columns[0] = 'Keys'
for idx,column in enumerate(columns[1:]):
  col_name = 'W{}'.format(idx)
  columns[idx+1]=col_name
dataset.columns = columns
keys = list(dataset.Keys)
for idx,key in enumerate(keys):
  keys[idx] = 'K{}'.format(idx)
dataset.Keys = keys
dataset.to_csv(path.replace(".csv", "_cleaned.csv"), index=False)
dataset_main = pd.read_csv("dataset/Sales_Transactions_Dataset_Weekly_cleaned.csv")
dataset = dataset_main
max_level = 4
p_value = 2
paa_value = 5
#Kapra Algorithm
QI_names = dataset.columns[1:]
id_col = dataset.columns[0]
min_attr,max_attr = Utility.get_min_max_attributes(dataset)
data_dict = dict()
for idx, row in dataset.iterrows():
  data_dict[row[id_col]] = list(row[QI_names])
good_leaves = list()
bad_leaves = list()
suppresed_nodes = list()
node = Node(level=1, group=data_dict, paa_value=paa_value)
node.start_split(p_value, max_level, good_leaves, bad_leaves)
Utility.recycle_bad_leaves(p_value, good_leaves,bad_leaves,suppresed_nodes,paa_value)