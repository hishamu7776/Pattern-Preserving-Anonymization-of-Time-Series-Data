

from turtle import st
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
        self.paa_value = paa_value
        if len(pr)==0:
            new_pr = "a"*self.paa_value
            self.pr = new_pr
        else:
            self.pr = pr

    def start_split(self,P,max_level,good_leaves,bad_leaves):
        if self.size < P:
            #Does not satisfies p-requirement, it will be labelled as bad leaf
            self.label = 'bad-leaf'
            bad_leaves.append(self)
            return
        
        if self.level == max_level:
            #SAX level reached maximum limit, labelled as good leaf
            self.label = 'good-leaf'
            good_leaves.append(self)
            return
        
        if P <= self.size < 2*P:
            '''
            This node is a good leaf as it satisfies p-requirement
            Splitting this will lead to generate atleast 1 bad leaf.
            '''
            self.maximize_level(max_level)
            self.label = 'good-leaf'
            good_leaves.append(self)
            return
        '''
        Checking node has to split by performing tentative splits. 
        '''
        level = self.level + 1
        tentative_child_nodes = dict()
        for key, time_series in self.group.items():
            pattern = Utility.find_pr(time_series,self.paa_value,level)
            if pattern in tentative_child_nodes.keys():
                tentative_child_nodes[pattern].append(key)
            else:
                tentative_child_nodes[pattern] = [key]
        '''
        Finding size of all tentative child nodes and checking for tentative nodes with more than P values.
        '''
        size_tcns = list()
        is_good_leaf = True
        for key in tentative_child_nodes:
            size_tcn = len(tentative_child_nodes[key])
            size_tcns.append(size_tcn)

        if is_good_leaf:
            '''
            If all tentative child node has fewer than p time series, the node will be labelled as good-leaf.
            and this will be termination of recursion.
            '''
            self.label = 'good-leaf'
            good_leaves.append(self)
            return
        else:
            '''
            Tentative child nodes can be splitted into subgroups.
            '''
            pr_keys = list(tentative_child_nodes.keys())
            pr_tg = list()
            tg_nodes_index = list(np.where(np.array(size_tcns) >= P)[0])
            tg_nodes = list()
            for idx in tg_nodes_index:
                tcn = tentative_child_nodes[pr_keys[idx]]
                dict_temp = dict()
                for key in tcn:
                    dict_temp[key] = self.group[key]
                tg_nodes.append(dict_temp)
                pr_tg.append(pr_keys[idx])
            pr_tb = list()  
            tb_nodes_index = list(np.where(np.array(size_tcns) < P)[0])
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
                node_merge = Node(level=self.level, pr=self.pr, label="good-leaf", group=child_merge, parent=self,paa_value=self.paa_value)
                self.child_node.append(node_merge)
                good_leaves.append(node_merge)
                nc = len(tg_nodes) + len(tb_nodes)
                if nc >= 2:
                    for idx in range(0, len(tg_nodes)):
                        node = Node(level=self.level, pr=pr_tg[idx], label="intermediate", group=tg_nodes[idx], parent=self,paa_value=self.paa_value)
                        self.child_node.append(node)
                        node.start_split(P, max_level, good_leaves, bad_leaves)
                else:
                    for idx in range(0, len(tg_nodes)):
                        node = Node(level=self.level, pr=pr_tg[idx], label="good-leaf", group=tg_nodes[idx], parent=self,paa_value=self.paa_value)
                        self.child_node.append(node)
                        good_leaves.append(node)
            else:
                nc = len(tg_nodes) + len(tb_nodes)
                for idx in range(0, len(tb_nodes)):
                    node = Node(level=self.level, pr=pr_tb[idx], label="bad-leaf", group=tb_nodes[idx], parent=self,paa_value=self.paa_value)
                    self.child_node.append(node)
                    bad_leaves.append(node)
                if nc >= 2:
                    for idx in range(0, len(tg_nodes)):
                        node = Node(level=self.level, pr=pr_tg[idx], label="intermediate", group=tg_nodes[idx], parent=self,paa_value=self.paa_value)
                        self.child_node.append(node)
                        node.start_split(P, max_level, good_leaves, bad_leaves)
                else:
                    for idx in range(0, len(tg_nodes)):
                        node = Node(level=self.level, pr=pr_tg[idx], label="good-leaf", group=tg_nodes[idx], parent=self,paa_value=self.paa_value)
                        self.child_node.append(node)
                        good_leaves.append(node)   


    def maximize_level(self, max_level):
        '''
        Maximize the level of node as long as the node has identical PR.
        '''
        values = list(self.group.values())
        iteration = True
        current_level = self.level
        pattern = None
        while iteration:
            level = self.level+1
            for time_series in values:
                if pattern is None:
                    pattern = Utility.find_pr(time_series,self.paa_value,level)
                else:
                    temp_pattern = pattern
                    pattern = Utility.find_pr(time_series,self.paa_value,level)
                    iteration = temp_pattern == pattern
                if iteration:
                    self.level = level
                    iteration = self.level <= max_level
        if current_level != self.level:
            self.pr = temp_pattern
