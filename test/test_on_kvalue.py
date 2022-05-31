import subprocess
import time
import script


'''
Experiment 1 : Try different k_values and check time efficiency of both algorithms
setting p_value to 2
paa_value = 10
setting attribute size = 100
setting table size = 1000
'''

file_name = 'timeseries.csv'
path = "datasets\\{}".format(file_name)
command = "python kp_anonymity.py {} {} {} {} {} {} {} {}"

k_values = [4,6,8,10,12]
kapra_k_exp_time = list()
naive_k_exp_time = list()
p_value = 2
paa_value = 10
dim = 100
size = 1000

for k_value in k_values:
    start_time = time.time()
    subprocess.call(command.format('naive', k_value, p_value, paa_value, path, "./output/k_values/output_k_{}_{}.csv".format('naive', k_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    naive_k_exp_time.append(exec_time)
    print("--- k value {} for naive completed in {} seconds ---".format(k_value,exec_time))
    start_time = time.time()
    subprocess.call(command.format('kapra', k_value, p_value, paa_value, path, "./output/k_values/output_k_{}_{}.csv".format('kapra', k_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    kapra_k_exp_time.append(exec_time)
    print("--- k value {} for kapra completed in {} seconds ---".format(k_value,exec_time))

script.draw_diagram("Time Efficiency on different K.", k_values, naive_k_exp_time, kapra_k_exp_time, "K", "Time Instances")