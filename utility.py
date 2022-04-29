import pandas as pd
import numpy as np
import logging
import datetime
from node import Node

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
def recycle_bad_leaves(P, good_leaves,bad_leaves,suppresed_nodes,paa_val):
  bad_nodes = dict()
  node_sizes = list()
  for node in bad_leaves:
    if node.level not in bad_nodes.keys():
      bad_nodes[node.level] = list()
    bad_nodes[node.level].append(node)
    node_sizes.append(node.size)
  current_level = max(bad_nodes.keys())
  bad_leaves_size = sum(node_sizes)
  while bad_leaves_size >= P:
    node_merge = dict()
    if len(bad_nodes[current_level])>1:
      for node in bad_nodes[current_level]:
        node_pr = node.pr
        if node_pr not in node_merge.keys():
          node_merge[node_pr] = list()
        node_merge[node_pr].append(node)
      for node_pr,nodes in node_merge.items():
        if len(nodes)>1:
          group = dict()          
          for node in nodes:
            group.update(node.group)
            bad_nodes[current_level].remove(node)
          new_leaf = Node(level=max(current_level,1), pr=node_pr,group=group, paa_value=paa_val)
          if new_leaf.size >= P:
            new_leaf.label = "good-leaf"
            good_leaves.append(new_leaf)
            bad_leaves_size = bad_leaves_size-new_leaf.size
          else:
            new_leaf.label = "bad-leaf"
            bad_nodes.append(new_leaf)
    
    for node in bad_nodes[current_level]:
      if current_level>2:
        values = list(node.group.values())
        pr_0 = find_pr(values,paa_val,current_level)
      else:
        pr_0 = pr = "a"*paa_val
      node.level = current_level-1
      node.pr = pr_0
    current_level = current_level-1
    if current_level < 0:
      break
    if current_level not in bad_nodes.keys():
      bad_nodes[current_level] = list()
    bad_nodes[current_level].extend(bad_nodes.pop(current_level+1))                             
  suppresed_nodes.extend(list(bad_nodes.values())[0])

def add_row_to_node(node_original, node_to_add):
      for key, value in node_to_add.group.items():
          node_original.group[key] = value
      node_original.members = list(node_original.group.keys())
      node_original.size = len(node_original.group)
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