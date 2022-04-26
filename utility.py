import pandas as pd
import numpy as np
import logging
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

def create_logging(path=None):
  file_name = "log_{}_{}_{}_{}_{}.txt".format(datetime.datetime.now().date().year, datetime.datetime.now().date().month, datetime.datetime.now().date().day, datetime.datetime.now().time().hour, datetime.datetime.now().time().minute)
  logger= logging.getLogger()
  logger.setLevel(logging.DEBUG) # or whatever
  #handler = logging.FileHandler(path+file_name, 'w', 'utf-8') # or whatever
  #handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
  #logger.addHandler(handler)
  return logger
def postprocessing(good_leaves, bad_leaves):
      difference = float('inf')
      for bad_leaf in bad_leaves:
            pattern_representation_bad_node = bad_leaf.pr
            choose_node = None            
            for index in range(0, len(good_leaves)):                
                pattern_representation_good_node = good_leaves[index].pr
                difference_good_bad = sum(1 for a, b in zip(pattern_representation_good_node,
                                                            pattern_representation_bad_node) if a != b)
                if difference_good_bad < difference:
                    choose_node = index
            # choose_node contain good node with minimum difference between pattern representation
            add_row_to_node(good_leaves[choose_node], bad_leaf)
      bad_leaves = list()

def add_row_to_node(node_original, node_to_add):
      for key, value in node_to_add.group.items():
          node_original.group[key] = value
      node_original.members = list(node_original.group.keys())
      node_original.size = len(node_original.group)