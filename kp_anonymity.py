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
        if k_value < p_value:
            print("Error:- Argument P value should be less than argument K value")
        else:
            dataset = pd.read_csv(path)            
            if algorithm == 'naive':
                naive = Naive(data=dataset,p_value=p_value,k_value=k_value,paa_value=paa_value)
                naive.run()
                print(naive.pattern_anonymized)
            elif algorithm == 'kapra':
                print(algorithm,k_value,p_value,paa_value)
            else:
                print('Error:- supported algorithms [naive, kapra]')
    else:
        print(" Error:- Please provide arguments in this order : k_value, p_value, paa_value, dataset path")
        print(" Usage :- python kp_anonymity.py algorithm k_value p_value paa_value input_path")
    '''
    kp_anonymized = dict()
    Utility.compute_anonymized_data(k_anonymized=anonymized_groups,p_anonymized=pattern_anonymized,kp_anonymized=kp_anonymized)
    Utility.save_anonymized('output.csv',kp_anonymized)
    '''