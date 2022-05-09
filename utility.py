import pandas as pd
import numpy as np
import datetime
import node

from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.alphabet import cuts_for_asize
from saxpy.sax import ts_to_string

#Common functions
def find_pr(ts,paa_val,level):
    '''
    A function to compute pattern representation of a timeseries
    Input : 
        ts      : timeseries
        paa_val : argument paa value
        level   : Level of pattern representation
    Output :
        pr : pattern representation of time series
    '''
    data = np.array(ts)
    data_znorm = znorm(data)
    data_paa = paa(data_znorm,paa_val)
    pr = ts_to_string(data_paa, cuts_for_asize(level))
    return pr

def create_anonymized_dataset(pattern_representation = None, anonymized_data=None, suppressed_data = list(), final_anonymized_data=None):
    for index,group in enumerate(anonymized_data):
        max_per_column = np.amax(np.array(list(group.values())),0)
        min_per_column = np.amin(np.array(list(group.values())),0)
        for key in group:
            row = list()
            for idx in range(0,len(max_per_column)):
                row.append("[{}-{}]".format(min_per_column[idx],max_per_column[idx]))
            row.append(pattern_representation[key])
            row.append('Group {}'.format(index))
            final_anonymized_data[key] = row

        if len(suppressed_data)>0:
            for index,group in enumerate(suppressed_data):
                for key in group:
                    row = list()
                    row.append('*')
                row.append('*')
                row.append('*')
                final_anonymized_data[key] = row 



def save_to_csv(path='',anonymized_data=None):
    with open(path,"w") as output_file:
        row = ""
        i=0
        for k,v in anonymized_data.items():
            row = "{},{}".format(k,",".join(v))
            output_file.write(row+"\n")
#functions for Naive method

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


#functions for kapra method
def max_vl(tuple_ts, data, tuple_key):
    max_value = 0
    max_vl_tuple = None
    for key in data:
        if key != tuple_key:
            vl = compute_instant_value_loss([tuple_ts, data[key]])
            if vl >= max_value:
                max_vl_tuple = key
    return max_vl_tuple  

def compute_instant_value_loss(table=None):
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
        upper_bound.append(ub)
        lower_bound.append(lb)
    return np.sqrt(sum(np.square(np.array(upper_bound)-np.array(lower_bound)))/tuple_size)*len(table)





