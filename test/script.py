import matplotlib.pyplot as plt
import subprocess
import time


def draw_diagram(title, x, y_naive, y_kapra, x_label, y_label):
    
    plt.figure(figsize=(12, 8))
    plt.plot(x, y_naive, color='red', marker='o', label='Naive Algorithm')
    plt.plot(x, y_kapra, color='green', marker='o', label='Kapra Algorithm')
    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.savefig('figures\\{}.png'.format(x_label))

    return


# Create new dataset
# python create_time_series.py start end type size filename[Optional]
'''
start = '2015-01-01'    # YYYY-MM-DD, YYYY-MM, YYYY
end = '2021-12-31'      # YYYY-MM-DD, YYYY-MM, YYYY
type = 'W'              # D, W, M, Y
size = 100000
'''
#data_generation = "python create_time_series.py {} {} {} {} {}".format(start,end,type,size,file_name)

# Clean dataset
# python clean_data.py path dim size
'''
path = 'dataset\\timeseries_dataset.csv'
num_attributes = 50 # Select subset of attributes
size = 700 # Select subset of data
data_generation = "python clean_data.py {} {} {}".format(path,num_attributes,size)
'''
# executing algorithm
'''
algorithm = 'naive' # kapra or naive
k_value = 4 # K value
p_value = 2 # P value
paa_value = 8 # paa value
path = "datasets\\{}".format(file_name)
output = "output_kapra_01.csv"
attributes = 50
size = 1000
command = "python kp_anonymity.py {} {} {} {} {} {} {} {} ".format(algorithm, k_value, p_value, paa_value, path, output, attributes, size)
'''
#subprocess.call(data_generation.split(), shell=True)

#subprocess.call(command.split(), shell=True)

