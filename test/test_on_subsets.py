import subprocess
import time
import script

'''
# Experiment 5 : Analysing time efficiency by changing size of table
# setting p_value = 4
# setting k_value = 8
# paa_value = 10
# setting table size = 2000
'''

file_name = 'timeseries.csv'
path = "datasets\\{}".format(file_name)
command = "python kp_anonymity.py {} {} {} {} {} {} {} {}"

num_time_series = [500,1000,2000,5000,10000]

kapra_size_exp_time = list()
naive_size_exp_time = list()
k_value = 8
p_value = 2
paa_value = 10
dim = 100

for size in num_time_series:
    start_time = time.time()
    subprocess.call(command.format('naive', k_value, p_value, paa_value, path, "./output/subsets/output_n_{}_{}.csv".format('naive', dim), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    naive_size_exp_time.append(exec_time)
    print("--- table size {} for naive completed in {} seconds ---".format(size, exec_time))
    start_time = time.time()
    subprocess.call(command.format('kapra', k_value, p_value, paa_value, path, "./output/subsets/output_n_{}_{}.csv".format('kapra', dim), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    kapra_size_exp_time.append(exec_time)
    print("--- table size {} for kapra completed in {} seconds ---".format(size, exec_time))


script.draw_diagram("Time efficiency on different sizes.", num_time_series, naive_size_exp_time, kapra_size_exp_time, "Number of time series", "Time Instance")
