

from tokenize import group
from turtle import st
import utility as Utility
import numpy as np

class Node:
    def __init__(self,level=1, pr="",label="intermediate",group=None,parent=None,paa_value=None):
        '''
        A Node contains multiple time series with same pattern representation
        Purpose: 
            Each node contains information about patterns and timeseries which follows the patterns.
        Input:
            level     : The sax level of current node. The patter representations are based on level 
            pr        : Pattern representation of current node
            label     : Whether the node is good-leaf, bad-leaf or intermediate
            group     : Set of timeseries.
            parent    : Parent node of current node
            paa_value : paa_value for time series    
        '''
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
        '''
        Stat split method will execute the splitting procedure of the node.
        Input:
            max_level  : Maximum level a node can have.
            P          : A node should contain atleas P timeseries.
            good_leaves: list of good leaves
            bad_leaves : list of bad leaves
        Output:
            lists of good and bad leaves.
            A tree node structure for each leaves.
        '''
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
            # This node is a good leaf as it satisfies p-requirement. 
            # Splitting this will lead to generate atleast 1 bad leaf.
            
            self.maximize_level(max_level)
            self.label = 'good-leaf'
            good_leaves.append(self)
            return
        # Checking node has to split by performing tentative splits. 
        level = self.level + 1
        tentative_child_nodes = dict()
        for key, time_series in self.group.items():
            pattern = Utility.find_pr(time_series,self.paa_value,level)
            if pattern in tentative_child_nodes.keys():
                tentative_child_nodes[pattern].append(key)
            else:
                tentative_child_nodes[pattern] = [key]
            
        # Finding size of all tentative child nodes and checking for tentative nodes with more than P values.
        size_tcns = list()
        for key in tentative_child_nodes:
            size_tcn = len(tentative_child_nodes[key])
            size_tcns.append(size_tcn)
        if np.all(np.array(size_tcns) < P):
            
            # If all tentative child node has fewer than p time series, the node will be labelled as good-leaf.
            # and this will be termination of recursion. The node cannot be splitted to child nodes.
            
            self.label = 'good-leaf'
            good_leaves.append(self)
            return
        else:
            
            # Tentative child nodes can be splitted into subgroups.
            # Seperate Tentative good nodes and tentative bad nodes.
            
            patterns = list(tentative_child_nodes.keys()) 
            tentative_good_node_patterns = list()
            tentative_good_nodes = list()
            tentative_bad_node_patterns = list()
            tentative_bad_nodes = list()
            for index, tentative_child_node in enumerate(tentative_child_nodes):
                if len(tentative_child_node) >= P:
                    tentative_good_node_keys = tentative_child_nodes[patterns[index]]
                    tentative_good_node = dict()
                    for tgn_key in tentative_good_node_keys:
                        tentative_good_node[tgn_key] = self.group[tgn_key]
                    tentative_good_nodes.append(tentative_good_node)
                    tentative_good_node_patterns.append(patterns[index])
                else:
                    tentative_bad_node_keys = tentative_child_nodes[patterns[index]]
                    tentative_bad_node = dict()
                    for tgn_key in tentative_bad_node_keys:
                        tentative_bad_node[tgn_key] = self.group[tgn_key]
                    tentative_bad_nodes.append(tentative_bad_node)
                    tentative_bad_node_patterns.append(patterns[index])

            # If total values in tentative bad nodes is greater than P, the node is labelled as good-lead with current level
            if sum([len(bad_node) for bad_node in tentative_bad_nodes]) >= P:
                merge_bad_nodes = dict()
                for bad_node in tentative_bad_nodes:
                    for key, value in bad_node.items():
                        merge_bad_nodes[key] = value
                child_merge = Node(level=self.level, pr=self.pr, label="good-leaf", group=merge_bad_nodes, parent=self,paa_value=self.paa_value)
                self.child_node.append(child_merge)
                good_leaves.append(child_merge)
                # If Total nodes nc are greater than 2, increase level. run splittling recursively. else label it as good leaf.
                nc = len(tentative_good_node) + len(tentative_bad_nodes)
                if nc >= 2:
                    for index, tantative_good_node in enumerate(tentative_good_nodes):
                        self.level = level
                        node = Node(level=self.level, pr=tentative_good_node_patterns[index], label="intermediate", group=tantative_good_node, parent=self, paa_value=self.paa_value)
                        node.start_split(P, max_level, good_leaves, bad_leaves)
                else:
                    for index, tantative_good_node in enumerate(tentative_good_nodes):
                        self.level = level
                        node = Node(level=self.level, pr=tentative_good_node_patterns[index], label="good-leaf", group=tantative_good_node, parent=self, paa_value=self.paa_value)
                        self.child_node.append(tentative_good_node)
            else:
                nc = len(tentative_good_node) + len(tentative_bad_nodes)
                self.level = level
                #if total bad leaves are less than P. label it as bad leaf.
                for index, tentative_bad_node in enumerate(tentative_bad_nodes):
                    node = Node(level=self.level, pr=tentative_bad_node_patterns[index], label="bad-leaf", group=tentative_bad_node, parent=self,paa_value=self.paa_value)
                    self.child_node.append(node)
                    bad_leaves.append(node)
                # If Total nodes nc are greater than 2, increase level. run splittling recursively. else label it as good leaf.
                if nc >= 2:
                    for index, tantative_good_node in enumerate(tentative_good_nodes):
                        node = Node(level=self.level, pr=tentative_good_node_patterns[index], label="intermediate", group=tentative_good_nodes[index], parent=self,paa_value=self.paa_value)
                        self.child_node.append(node)
                        node.start_split(P, max_level, good_leaves, bad_leaves)
                else:
                    for index, tantative_good_node in enumerate(tentative_good_nodes):
                        node = Node(level=self.level, pr=tentative_good_node_patterns[index], label="good-leaf", group=tentative_good_nodes[index], parent=self,paa_value=self.paa_value)
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
