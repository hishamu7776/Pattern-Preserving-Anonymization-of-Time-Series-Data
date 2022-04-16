import random
import numpy as np
import utility as Utility


def topdown_greedy(data=None, k_val=None, max_val=None, min_val=None, k_anonymized=None,columns=None):
  key_list = list(data.keys())
  size = len(key_list)
  if size<2*k_val:
    k_anonymized.append(data)
    return
  else:
    rounds = 3
    rand_tuple = key_list[random.randint(0, len(key_list) - 1)]
    group_u = dict()
    group_v = dict()
    group_u[rand_tuple] = data[rand_tuple]
    del data[rand_tuple]
    last_row = rand_tuple
    for round in range(0, rounds*2 - 1):
      if len(data)>0:
        if round % 2 == 0:
          v = Utility.max_ncp(group_u[last_row], data, last_row, max_val, min_val)
          group_v[v] = data[v]
          last_row = v
          del data[v]
        else:
          u = Utility.max_ncp(group_v[last_row], data, last_row, max_val, min_val)
          group_u[u] = data[u]
          last_row = u
          del data[u]
    key_indexes = [idx for idx in range(0, len(data.keys()))]
    random.shuffle(key_indexes)
    keys = [list(data.keys())[i] for i in key_indexes]
    for key in keys:
      temp_row = data[key]
      group_u_values = list(group_u.values())
      group_v_values = list(group_v.values())
      group_u_values.append(temp_row)
      group_v_values.append(temp_row)
      ncp_u = Utility.compute_ncp(group_u_values, max_val, min_val)
      ncp_v = Utility.compute_ncp(group_v_values, max_val, min_val)
      if ncp_v < ncp_u:
        group_v[key] = temp_row
      else:
        group_u[key] = temp_row
      del data[key]
    if len(group_u) > k_val:
      topdown_greedy(data=group_u, k_val=k_val, max_val=max_val, min_val=min_val,k_anonymized=k_anonymized)
    else:
      k_anonymized.append(group_u)
      
    if len(group_v) > k_val:
      topdown_greedy(data=group_v, k_val=k_val, max_val=max_val, min_val=min_val,k_anonymized=k_anonymized)
    else:
      k_anonymized.append(group_v)
    return
