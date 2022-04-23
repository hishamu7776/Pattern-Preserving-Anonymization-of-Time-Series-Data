

import utility as Utility
import numpy as np

class Node:
  def __init__(self,level=1, pr="",label="intermediate",group=None,parent=None,paa_value=None):
    self.level = level
    self.members = list(group.keys())
    self.size = len(group)
    self.label = label
    self.group = group
    self.child_node = list()
    self.parent = parent
    if len(pr)==0:
      new_pr = "a"*self.paa_value
      self.pr = new_pr
    else:
      self.pr = pr
  def start_split(self,P,max_level,good_leaves,bad_leaves):
    if self.size < P:
      self.label = 'bad-leaf'
      bad_leaves.append(self)
      return
    if self.level == max_level:
      self.label = 'good-leaf'
      good_leaves.append(self)
      return
    if self.size >= P and self.size < 2*P:
      self.maximize_level(max_level)
      self.label = 'good-leaf'
      good_leaves.append(self)
      return
    
    tentative_child_nodes = dict()
    temp_level = self.level + 1
    for k, v in self.group.items():
      pr_0 = Utility.find_pr(v,self.paa,temp_level)
      if pr_0 in tentative_child_nodes.keys():
        tentative_child_nodes[pr_0].append(k)
      else:
        tentative_child_nodes[pr_0] = [k]
    size_of_tcns = [len(tentative_child_nodes[key]) for key in tentative_child_nodes]
    is_good_leaf = np.all(np.array(size_of_tcns) < P)
    if is_good_leaf:
      self.label = 'good-leaf'
      good_leaves.append(self)
      return
    else:
      pr_keys = list(tentative_child_nodes.keys())
      pr_tg = list()
      tg_nodes_index = list(np.where(np.array(size_of_tcns) >= P)[0])
      tg_nodes = list()
      for idx in tg_nodes_index:
        tcn = tentative_child_nodes[pr_keys[idx]]
        dict_temp = dict()
        for key in tcn:
          dict_temp[key] = self.group[key]
        tg_nodes.append(dict_temp)
        pr_tg.append(pr_keys[idx])
      
      pr_tb = list()  
      tb_nodes_index = list(np.where(np.array(size_of_tcns) < P)[0])
      tb_nodes = list()
      for idx in tb_nodes_index:
        tcn = tentative_child_nodes[pr_keys[idx]]
        dict_temp = dict()
        for key in tcn:
          dict_temp[key] = self.group[key]
        tb_nodes.append(dict_temp)
        pr_tb.append(pr_keys[idx])
      tb_nodes_size = 0
      for tb_node in tb_nodes:
        tb_nodes_size+len(tb_node)
      if tb_nodes_size >= P:
        child_merge = dict()
        for tb_node in tb_nodes:
          for k, v in tb_node.items():
            child_merge[k] = v
        node_merge = Node(level=self.level, pr=self.pr, label="good-leaf", group=child_merge, parent=self)
        self.child_node.append(node_merge)
        good_leaves.append(node_merge)
        nc = len(tg_nodes) + len(tb_nodes)
        if nc >= 2:
          for idx in range(0, len(tg_nodes)):
            node = Node(level=self.level, pr=pr_tg[idx], label="intermediate", group=tg_nodes[idx], parent=self)
            self.child_node.append(node)
            node.start_splitting(P, max_level, good_leaves, bad_leaves)
        else:
          for idx in range(0, len(tg_nodes)):
            node = Node(level=self.level, pr=pr_tg[idx], label="good-leaf", group=tg_nodes[idx], parent=self)
            self.child_node.append(node)
            good_leaves.append(node)
      else:
        nc = len(tg_nodes) + len(tb_nodes)
        for idx in range(0, len(tb_nodes)):
          node = Node(level=self.level, pr=pr_tb[idx], label="bad-leaf", group=tb_nodes[idx], parent=self)
          self.child_node.append(node)
          bad_leaves.append(node)
          if nc >= 2:
            for idx in range(0, len(tg_nodes)):
              node = Node(level=self.level, pr=pr_tg[idx], label="intermediate", group=tg_nodes[idx], parent=self)
              self.child_node.append(node)
              node.start_splitting(P, max_level, good_leaves, bad_leaves)
          else:
            for idx in range(0, len(tg_nodes)):
              node = Node(level=self.level, pr=pr_tg[idx], label="good-leaf", group=tg_nodes[idx], parent=self)
              self.child_node.append(node)
              good_leaves.append(node)

    
  def maximize_level(self, max_level):
    values = list(self.group.values())
    current_level = self.level
    equal = True
    while True and self.level < max_level:
      temp_level = self.level+1
      pr_1 = Utility.find_pr(values[0],self.paa,temp_level)
      for idx in range(1,len(values)):
        pr_2 = Utility.find_pr(values[idx],self.paa,temp_level)
        if pr_2 != self.pr:
          equal = False
          break
      if equal:
        self.level = temp_level
    if current_level != self.level:
      self.pr = Utility.find_pr(np.array(values[0]),self.paa,self.level)