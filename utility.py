import pandas as pd
import numpy as np
import datetime
import node

from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.alphabet import cuts_for_asize
from saxpy.sax import ts_to_string

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
def max_vl(tuple_ts, data, tuple_key, max_val, min_val):
    max_value = 0
    max_vl_tuple = None
    for key in data:
        if key != tuple_key:
            vl = compute_instant_value_loss([tuple_ts, data[key]])
            if vl >= max_value:
                max_vl_tuple = key
    return max_vl_tuple  

def compute_instant_value_loss(table=None , max_val=None, min_val=None):
    lower_bound = list()
    upper_bound = list()
    tuple_size = len(table[0])
    for idx in range(0,tuple_size):        
        lb = float('inf')
        ub = 0
        for row in table:
            if row[idx] > ub:
                ub = row[idx]
            if row[idx] < lb:
                lb = row[idx]
        upper_bound.append(z1_temp)
        lower_bound.append(y1_temp)
    return np.sqrt(sum(np.square(np.array(upper_bound)-np.array(lower_bound)))/tuple_size)*len(table)
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



def compute_anonymized_data(k_anonymized=None, p_anonymized=None,kp_anonymized=None):
  for i in range(0,len(k_anonymized)):
    group = k_anonymized[i]
    list_good_leaf = p_anonymized[i]
    max_val = np.amax(np.array(list(group.values())),0)
    min_val = np.amin(np.array(list(group.values())),0)
    for key in group.keys():
      kp_anonymized[key] = list()
      row = list()
      for idx in range(0,len(max_val)):
        row.append("[{}-{}]".format(min_val[idx],max_val[idx]))
      for node in list_good_leaf:
        if key in node.group.keys():
          row.append(node.pr)
      row.append("Group: {}".format(i))
      kp_anonymized[key] = row
def save_anonymized(path,kp_anonymized):
  with open(path,"w") as output_file:
    row = ""
    for k,v in kp_anonymized.items():
      row = "{},{}".format(k,",".join(v))
      output_file.write(row+"\n")