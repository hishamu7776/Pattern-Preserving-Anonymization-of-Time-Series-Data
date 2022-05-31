import subprocess
import time
import script

'''
Experiment 2 : Trying different p_values and check time efficiency
setting k_value = 8
paa_value = 10
setting attribute size = 100
setting table size = 1000
'''

file_name = 'timeseries.csv'
path = "datasets\\{}".format(file_name)
command = "python kp_anonymity.py {} {} {} {} {} {} {} {}"


p_values = [2, 3, 4, 5, 6] 

kapra_p_exp_time = list()
naive_p_exp_time = list()
k_value = 8
paa_value = 10
dim = 100
size = 2000

for p_value in p_values:
    start_time = time.time()
    subprocess.call(command.format('naive', k_value, p_value, paa_value, path, "./output/p_values/output_p_{}_{}.csv".format('naive', p_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    naive_p_exp_time.append(exec_time)
    print("--- p_value {} for naive completed in {} seconds ---".format(p_value,exec_time))
    start_time = time.time()
    subprocess.call(command.format('kapra', k_value, p_value, paa_value, path, "./output/p_values/output_p_{}_{}.csv".format('kapra', p_value), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    kapra_p_exp_time.append(exec_time)
    print("--- p_value {} for kapra completed in {} seconds ---".format(p_value,exec_time))


script.draw_diagram("Time Efficiency on different P.", p_values, naive_p_exp_time, kapra_p_exp_time, "P", "Time Instances")