import pandas as pd
import numpy as np
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.alphabet import cuts_for_asize
from saxpy.sax import ts_to_string

def clean_data(path='dataset/dataset.csv',final_column=''):
    dataset = pd.read_csv(path)
    columns = list(dataset.columns)
    idx = columns.index(final_column)
    dataset = dataset[columns[0:idx+1]]
    dataset.to_csv(path.replace(".csv", "_Final.csv"), index=False)

def get_min_max_attributes(table):
  min_attribute_values = list()
  max_attribute_values = list()
  for col in table.columns[1:]:
    min_attribute_values.append(table[col].min())
    max_attribute_values.append(table[col].max())
  return min_attribute_values,max_attribute_values

def max_ncp(tuple_ts, data, tuple_key, max_val, min_val):
    max_value = 0
    max_ncp_tuple = None
    for key in data:
        if key != tuple_key:
            ncp = compute_ncp([tuple_ts, data[key]], max_val, min_val)
            if ncp >= max_value:
                max_ncp_tuple = key
    return max_ncp_tuple  

def compute_ncp(table=None , max_val=None, min_val=None):
    z1 = list()
    y1 = list()
    A = list()
    tuple_size = len(table[0])
    table_size = len(table)
    for idx in range(0,tuple_size):
        z1_temp = 0
        y1_temp = float('inf')
        for row in table:
            if row[idx] > z1_temp:
                z1_temp = row[idx]
            if row[idx] < y1_temp:
                y1_temp = row[idx]
        z1.append(z1_temp)
        y1.append(y1_temp)
        A.append(abs(max_val[idx] - min_val[idx]))
    ncp_t = 0
    for idx in range(0, len(z1)):
        if A[idx]!=0:
            ncp_t += (z1[idx] - y1[idx]) / A[idx]
        else:
            ncp_t += 0
    ncp_T = table_size*ncp_t
    return ncp_T
  
def find_pr(ts,paa_val,level):
    data = np.array(ts)
    data_znorm = znorm(data)
    data_paa = paa(data_znorm,paa_val)
    pr = ts_to_string(data_paa, cuts_for_asize(level))
    return pr