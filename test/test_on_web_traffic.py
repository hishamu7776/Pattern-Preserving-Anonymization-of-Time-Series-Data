import subprocess
import time
import script
import value_loss_metric
import os
import pandas as pd

file_name = 'web_traffic.csv'
path = "datasets\\{}".format(file_name)
command = "python kp_anonymity.py {} {} {} {} {} {} {} {}"
'''
k_values = [4,6,8,10,12]
kapra_k_exp_time = list()
naive_k_exp_time = list()
p_value = 2
paa_value = 8
dim = 240
size = 5000

for k_value in k_values:
    start_time = time.time()
    subprocess.call(command.format('naive', k_value, p_value, paa_value, path, "./output/web_traffic/output_k_{}_{}.csv".format('naive', k_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    naive_k_exp_time.append(exec_time)
    print("--- k value {} for naive completed in {} seconds ---".format(k_value,exec_time))
    start_time = time.time()
    subprocess.call(command.format('kapra', k_value, p_value, paa_value, path, "./output/web_traffic/output_k_{}_{}.csv".format('kapra', k_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    kapra_k_exp_time.append(exec_time)
    print("--- k value {} for kapra completed in {} seconds ---".format(k_value,exec_time))

script.draw_diagram("Time Efficiency on different K.", k_values, naive_k_exp_time, kapra_k_exp_time, "K", "Time Instances")
p_values = [2, 3, 4, 5, 6] 

kapra_p_exp_time = list()
naive_p_exp_time = list()
k_value = 10
paa_value = 8
dim = 240
size = 5000

for p_value in p_values:
    start_time = time.time()
    subprocess.call(command.format('naive', k_value, p_value, paa_value, path, "./output/web_traffic/output_p_{}_{}.csv".format('naive', p_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    naive_p_exp_time.append(exec_time)
    print("--- p_value {} for naive completed in {} seconds ---".format(p_value,exec_time))
    start_time = time.time()
    subprocess.call(command.format('kapra', k_value, p_value, paa_value, path, "./output/web_traffic/output_p_{}_{}.csv".format('kapra', p_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    kapra_p_exp_time.append(exec_time)
    print("--- p_value {} for kapra completed in {} seconds ---".format(p_value,exec_time))


script.draw_diagram("Time Efficiency on different P.", p_values, naive_p_exp_time, kapra_p_exp_time, "P", "Time Instances")
'''
x_label_k = list()
x_label_p = list()
value_loss_k = {"naive":[],"kapra":[]}
value_loss_p = {"naive":[],"kapra":[]}

for file_name in os.listdir('output/web_traffic'):
    info = file_name.split('_')
    anonymized = pd.read_csv(os.path.join('output/web_traffic',file_name), header=None,sep=',', on_bad_lines='skip')
    if info[1] == 'k':                
        if info[2]=='kapra':
            x_label_k.append(int(info[3].split('.')[0]))
            value_loss_k['kapra'].append(value_loss_metric.find_value_loss(anonymized))
        elif info[2]=='naive':
            value_loss_k['naive'].append(value_loss_metric.find_value_loss(anonymized))
    elif info[1] == 'p':                
        if info[2]=='kapra':
            x_label_p.append(int(info[3].split('.')[0]))
            value_loss_p['kapra'].append(value_loss_metric.find_value_loss(anonymized))
        elif info[2]=='naive':
            value_loss_p['naive'].append(value_loss_metric.find_value_loss(anonymized))

value_loss_metric.plot_barchart(x_label_k, value_loss_k, "K value")
value_loss_metric.plot_barchart(x_label_p, value_loss_p, "P value")
