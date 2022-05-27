from kapra import *
from naive import *
from utility import *
from top_down import *

import os
import numpy as np
import pandas as pd
import sys
import random


if __name__ == "__main__":
    if len(sys.argv) == 6:
        algorithm = sys.argv[1]
        k_value = int(sys.argv[2])
        p_value = int(sys.argv[3])
        paa_value = int(sys.argv[4])
        path = sys.argv[5]
        final_anonymized_data = dict()        
        if k_value < p_value:
            print("Error:- Argument P value should be less than argument K value")
        else:
            dataset = pd.read_csv(path)            
            if algorithm == 'naive':
                naive = Naive(data=dataset,p_value=p_value,k_value=k_value,paa_value=paa_value)
                naive.run()
                output_path = os.path.join('output\\naive',path.split('\\')[-1])
                Utility.create_anonymized_dataset(pattern_representation = naive.pattern_map, anonymized_data=naive.k_anonymized_data, final_anonymized_data=final_anonymized_data)
                Utility.save_to_csv(path=output_path,anonymized_data=final_anonymized_data)
            elif algorithm == 'kapra':
                kapra = Kapra(data=dataset, p_value=p_value, k_value=k_value, paa_value=paa_value, max_level=4)
                kapra.run()
                output_path = os.path.join('output\\kapra',path.split('\\')[-1])
                Utility.create_anonymized_dataset(pattern_representation = kapra.pattern_map, anonymized_data=kapra.group_list, suppressed_data=kapra.suppressed_nodes_list, final_anonymized_data=final_anonymized_data)
                Utility.save_to_csv(path=output_path,anonymized_data=final_anonymized_data)
            else:
                print('Error:- supported algorithms [naive, kapra]')
    else:
        print(" Error:- Please provide arguments in this order : k_value, p_value, paa_value, dataset path")
        print(" Usage :- python kp_anonymity.py algorithm k_value p_value paa_value input_path")