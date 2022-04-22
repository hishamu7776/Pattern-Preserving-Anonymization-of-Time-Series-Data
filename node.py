

import utility as Utility

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
      pr_0 = find_pr(v,self.paa,temp_level)
      if pr_0 in tentative_child_nodes.keys():
        tentative_child_nodes[pr_0].append(k)
      else:
        tentative_child_nodes[pr_0] = [k]
    size_of_tcns = [len(tentative_child_nodes[key]) for key in tentative_child_nodes]
    
  def maximize_level(self, max_level):
    values = list(self.group.values())
    current_level = self.level
    equal = True
    while True and self.level < max_level:
      temp_level = self.level+1
      pr_1 = find_pr(values[0],self.paa,temp_level)
      for idx in range(1,len(values)):
        pr_2 = find_pr(values[i],self.paa,temp_level)
        if pr_2 != pr:
          equal = False
          break
      if equal:
        self.level = temp_level
    if current_level != self.level:
      self.pr = find_pr(np.array(values_group[0]),self.paa,self.level)