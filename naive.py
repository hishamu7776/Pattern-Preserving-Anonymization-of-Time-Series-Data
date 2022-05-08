import os
import random

import numpy as np
import pandas as pd
import utility as Utility
import top_down as TopDown
from node import *
class Naive:
  def __init__(self,data=None,p_value=None,k_value=None,paa_value=None,max_level=4):
    if p_value!=None:
      self.p_value = p_value
    else:
      self.p_value = 3
    if k_value != None:
      self.k_value = k_value
    else:
      self.k_value = 4
    if paa_value != None:
      self.paa_value = paa_value
    else:
      self.paa_value = 5
    self.data = data
    self.max_level=max_level
    self.k_anonymized_data = list()
    self.pattern_anonymized = list()

  def run(self):
    QI_names = self.data.columns[1:]
    id_col = self.data.columns[0]
    min_attr,max_attr = Utility.get_min_max_attributes(self.data)
    data_dict = dict()
    for idx, row in self.data.iterrows():
      data_dict[row[id_col]] = list(row[QI_names])
    duplicate = data_dict.copy()
    TopDown.topdown_greedy(data=duplicate, k_val=self.k_value, max_val=max_attr, min_val=min_attr, k_anonymized=self.k_anonymized_data,columns=QI_names)
    anonymized_groups = list()
    for group in self.k_anonymized_data:
      anonymized_groups.append(group)
      good_leaves = list()
      bad_leaves = list()
      node = Node(level=1, group=group, paa_value=self.paa_value)
      node.start_splitting(self.p_value, self.max_level, good_leaves, bad_leaves)
      if len(bad_leaves) > 0:
        Naive.postprocessing(good_leaves, bad_leaves)
      self.pattern_anonymized.append(good_leaves)

  @staticmethod
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
            Naive.add_row_to_node(good_leaves[choose_node], bad_leaf)
      bad_leaves = list()
  
  @staticmethod
  def add_row_to_node(node_original, node_to_add):
      for key, value in node_to_add.group.items():
          node_original.group[key] = value
      node_original.members = list(node_original.group.keys())
      node_original.size = len(node_original.group)
    
