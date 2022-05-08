import os
import random

import numpy as np
import pandas as pd
import utility as Utility
import top_down as TopDown
import node

class Kapra:
    def __init__(
        self, data=None, p_value=None, k_value=None, paa_value=None, max_level=4
    ):
        self.p_value = p_value
        self.k_value = k_value
        self.k_value = 4
        self.paa_value = paa_value
        self.data = data
        self.max_level = max_level

    def run(self):
        dataset = self.data.copy()
        columns = dataset.columns[1:]
        id_col = dataset.columns[0]
        min_attr, max_attr = Utility.get_min_max_attributes(dataset)
        data_dict = dict()
        for idx, row in dataset.iterrows():
            data_dict[row[id_col]] = list(row[columns])
        good_leaves = list()
        bad_leaves = list()
        suppresed_nodes = list()
        node = Node(level=1, group=data_dict, paa_value=self.paa_value)
        node.start_split(self.p_value, self.max_level, good_leaves, bad_leaves)
        Kapra.recycle_bad_leaves(
            self.p_value, good_leaves, bad_leaves, suppresed_nodes, self.paa_value
        )
        suppressed_nodes_list = list()
        for node in suppresed_nodes:
            suppressed_nodes_list.append(node.group)

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
