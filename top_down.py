import random
from re import A
from turtle import update
import numpy as np
import utility as Utility

class TopDownGreedy:
    
    def __init__(self, k_val=None, max_val=None, min_val=None, k_anonymized=None,columns=None,method=None):
        self.k_value = k_val
        self.max_value = max_val
        self.min_value = min_val
        self.k_anonymized = k_anonymized
        self.columns = columns
        self.method = method
        self.neighbours = list()
        self.flag = False


    def topdown_greedy(self,data=None, name='r'):
        key_list = list(data.keys())
        size = len(key_list)
        if size<2*self.k_value:
            self.k_anonymized.append(data)
            self.neighbours.append(name)
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
                        if self.method=='ncp':
                            v = Utility.max_ncp(group_u[last_row], data, last_row, self.max_value, self.min_value)
                        elif self.method=='vl':
                            v = Utility.max_vl(group_u[last_row], data, last_row)
                        group_v[v] = data[v]
                        last_row = v
                        del data[v]
                    else:
                        if self.method=='ncp':
                            u = Utility.max_ncp(group_v[last_row], data, last_row, self.max_value, self.min_value)
                        elif self.method=='vl':
                            u = Utility.max_vl(group_v[last_row], data, last_row)
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
                if self.method=='ncp':
                    res_u = Utility.compute_ncp(group_u_values, self.max_value, self.min_value)
                    res_v = Utility.compute_ncp(group_v_values, self.max_value, self.min_value)
                elif self.method=='vl':
                    res_v = Utility.compute_instant_value_loss(group_v_values)
                    res_u = Utility.compute_instant_value_loss(group_u_values)
                if res_v < res_u:
                    group_v[key] = temp_row
                else:
                    group_u[key] = temp_row
                del data[key]
            
            if len(group_u) > self.k_value:
                self.topdown_greedy(data = group_u, name=name+'u')
            else:
                self.k_anonymized.append(group_u) 
                self.neighbours.append(name)


            if len(group_v) > self.k_value:
                self.topdown_greedy(data = group_v, name = name+'v')
            else:
                self.k_anonymized.append(group_v)  
                self.neighbours.append(name)                               
            return

    def postprocessing(self):
        '''
         If one group G has less than k tuples, we apply the local greedy adjustment similar to the bottom-up approach.

        '''
        #delete group if fully merged to neighbour, update group if merge with other group and delete remaining group.
        delete_list = list()
        for group_idx,group in enumerate(self.k_anonymized):
            group_size = len(group)
            if group_size < self.k_value:
                '''
                First, we can find a set G' of (k - |G|) tuples in some other group that has more than (2k - |G|) tuples such that NCP(G U G') is minimized.
                '''
                g_prime_size = self.k_value-group_size
                loss_measure_og = float('inf')                
                for index,other_group in enumerate(self.k_anonymized):
                    remaining_group_after_merge = other_group.copy()
                    if len(other_group) >= (2*self.k_value-group_size):
                        to_be_merged_og = group.copy()
                        to_be_merged_values = list(to_be_merged_og.values())
                        loss_measurement = float('inf')
                        for iteration in range(g_prime_size):
                            for key,value in other_group.items():
                                if self.method == 'ncp':
                                    temp_measurement = Utility.compute_ncp( to_be_merged_values+[value], self.max_value, self.min_value)
                                else:
                                    temp_measurement = Utility.compute_instant_value_loss(to_be_merged_values+[value])
                                if temp_measurement<loss_measurement:
                                    loss_measurement = temp_measurement
                                    selected_group = { key:value }
                                    del remaining_group_after_merge[key]
                            to_be_merged_og.update(selected_group)
                        if loss_measurement<loss_measure_og:
                            loss_measure_og = loss_measurement
                            changed_group_index = index
                
                '''
                Second, we compute the increase of penalty by merging G with the nearest neighbor group of G.
                '''
                neighbour_index = TopDownGreedy.find_neighbour_node(neighbours = self.neighbours, group_index = group_idx)
                loss_measure_neighbour = float('inf')
                to_be_merged_neighbour = self.k_anonymized[neighbour_index].copy()
                if neighbour_index != None:
                    to_be_merged_neighbour.update(group)
                    if self.method == 'ncp':
                        loss_measure_neighbour = Utility.compute_ncp( list(to_be_merged_neighbour.values()), self.max_value, self.min_value)
                    else:
                        loss_measure_neighbour = Utility.compute_instant_value_loss(list(to_be_merged_neighbour.values()))
                                        
                if loss_measure_neighbour < loss_measure_og:
                    delete_list.append(group_idx)
                    self.k_anonymized[neighbour_index] = to_be_merged_neighbour
                else:
                    self.k_anonymized[group_idx] = to_be_merged_og
                    self.k_anonymized[changed_group_index] = remaining_group_after_merge

        new_k_anonymised_list = list()        
        for index, group in enumerate(self.k_anonymized):
            if index not in delete_list:
                new_k_anonymised_list.append(group)                            
        for index in delete_list:
            del self.neighbours[index]

        self.k_anonymized = new_k_anonymised_list        
        self.flag = np.all(np.array([len(group) for group in new_k_anonymised_list]) < self.k_value)

        return

    @staticmethod
    def find_neighbour_node(neighbours = None, group_index = None):
        neighbour_index = 0
        group_name = neighbours[group_index]
        for index, name in enumerate(neighbours):
            if group_index != index:
                if name[:-1] == group_name[:-1]:
                    neighbour_index = index
                    break
        return neighbour_index