import subprocess
import time
import script

'''
# Experiment 4 : Analysing time efficiency by changing number of attributes
# setting p_value = 4
# setting k_value = 8
# paa_value = 10
# setting table size = 1000
'''

file_name = 'timeseries.csv'
path = "datasets\\{}".format(file_name)
command = "python kp_anonymity.py {} {} {} {} {} {} {} {}"

attribute_size = [50,100,150,200,250,300,350,400]


kapra_dim_exp_time = list()
naive_dim_exp_time = list()
k_value = 8
p_value = 2
paa_value = 10
size = 1000

for dim in attribute_size:
    start_time = time.time()
    subprocess.call(command.format('naive', k_value, p_value, paa_value, path, "./output/subsets/output_attr_{}_{}.csv".format('naive', dim), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    naive_dim_exp_time.append(exec_time)
    print("--- attribute size {} for naive completed in {} seconds ---".format(dim,exec_time))
    start_time = time.time()
    subprocess.call(command.format('kapra', k_value, p_value, paa_value, path, "./output/subsets/output_attr_{}_{}.csv".format('kapra', dim), dim, size).split(), shell=True)
    exec_time = time.time() - start_time
    kapra_dim_exp_time.append(exec_time)
    print("--- attribute size {} for kapra completed in {} seconds ---".format(dim,exec_time))

script.draw_diagram("Time efficiency on different attribute size", attribute_size, naive_dim_exp_time, kapra_dim_exp_time, "Attribute size", "Time Instance")
