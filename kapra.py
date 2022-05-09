from node import *

import os
import random

import numpy as np
import pandas as pd
import utility as Utility
import top_down as TopDown


class Kapra:
    def __init__(self, data=None, p_value=None, k_value=None, paa_value=None, max_level=4):
        self.p_value = p_value
        self.k_value = k_value
        self.k_value = 4
        self.paa_value = paa_value
        self.data = data
        self.max_level = max_level
        self.pattern_map = dict()
        self.group_list = list()
        self.suppressed_nodes_list = list()

    def run(self):
        dataset = self.data.copy()
        column_list = dataset.columns[1:]
        id_col = dataset.columns[0]
        data_dict = dict()
        for idx, row in dataset.iterrows():
            data_dict[row[id_col]] = list(row[column_list])
        good_leaves = list()
        bad_leaves = list()
        node = Node(level=1, group=data_dict, paa_value=self.paa_value)
        node.start_split(self.p_value, self.max_level, good_leaves, bad_leaves)
        suppressed_nodes = list()
        Kapra.recycle_bad_leaves(self.p_value, good_leaves,bad_leaves,suppressed_nodes,self.paa_value)
        for node in suppressed_nodes:
            self.suppressed_nodes_list.append(node.group)
        p_group_after_split = list()
        p_group_list = list()
        for idx,node in enumerate(good_leaves):
            group = node.group
            for key in group.keys():
                self.pattern_map[key] = node.pr           
            if node.size >= 2*self.p_value:
                group_to_split = group.copy()
                TopDown.topdown_greedy(data=group_to_split, k_val=self.p_value, k_anonymized=p_group_after_split,columns=column_list,ncp_or_vl='vl')
            else:
                p_group_list.append(group)
        p_group_list.extend(p_group_after_split) 
        #step 1
        pgl_size = 0
        for group in p_group_list:
            if len(group.keys())>=self.k_value:
                self.group_list.append(group)
                p_group_list.remove(group)
        else:
            pgl_size=pgl_size+len(group.keys())   
        #Iteration - Step 2 - 4
        while pgl_size>=self.k_value:
            G = Kapra.find_k_group_with_minimum_vl(pgl=p_group_list)
            pgl_size = pgl_size - len(G)
            while len(G.keys())<self.k_value:
                G_temp = Kapra.find_k_group_with_minimum_vl(pgl=p_group_list,new_group=G)
                G.update(G_temp)
                pgl_size = pgl_size - len(G_temp)
            self.group_list.append(G)

        for group in p_group_list:
            G = Kapra.find_k_group_with_minimum_vl(pgl=self.group_list,new_group=group)
            group.update(G)
            self.group_list.append(group)
        

    @staticmethod
    def recycle_bad_leaves(P, good_leaves, bad_leaves, suppresed_nodes, paa_val):
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
            if len(bad_nodes[current_level]) > 1:
                for node in bad_nodes[current_level]:
                    node_pr = node.pr
                    if node_pr not in node_merge.keys():
                        node_merge[node_pr] = list()
                    node_merge[node_pr].append(node)
                for node_pr, nodes in node_merge.items():
                    if len(nodes) > 1:
                        group = dict()
                        for node in nodes:
                            group.update(node.group)
                            bad_nodes[current_level].remove(node)
                        new_leaf = Node(
                            level=max(current_level, 1),
                            pr=node_pr,
                            group=group,
                            paa_value=paa_val,
                        )
                        if new_leaf.size >= P:
                            new_leaf.label = "good-leaf"
                            good_leaves.append(new_leaf)
                            bad_leaves_size = bad_leaves_size - new_leaf.size
                        else:
                            new_leaf.label = "bad-leaf"
                            bad_nodes.append(new_leaf)

            for node in bad_nodes[current_level]:
                if current_level > 2:
                    values = list(node.group.values())
                    pr_0 = Utility.find_pr(values, paa_val, current_level)
                else:
                    pr_0 = pr = "a" * paa_val
                node.level = current_level - 1
                node.pr = pr_0
            current_level = current_level - 1
            if current_level < 0:
                break
            if current_level not in bad_nodes.keys():
                bad_nodes[current_level] = list()
            bad_nodes[current_level].extend(bad_nodes.pop(current_level + 1))
        suppresed_nodes.extend(list(bad_nodes.values())[0])

    @staticmethod
    def find_k_group_with_minimum_vl(pgl=None,new_group=dict()):
        cur_vl = float("inf")
        group_with_min_vl = dict()
        minimal_index = 0
        for idx,group in enumerate(pgl):
            vl = Utility.compute_instant_value_loss(list(group.values())+list(new_group.values()))    
            if vl < cur_vl:
                cur_vl = vl
                group_with_min_vl = group
                minimal_index = idx
        if len(pgl)>0:
            del pgl[minimal_index]  
        return group_with_min_vl