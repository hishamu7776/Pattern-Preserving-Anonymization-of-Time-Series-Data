import pandas as pd
import numpy as np
import random
import sys
import os

'''
python create_time_series.py start end type size filename[Optional]

start : beginning of time : YYYY or YYYY-MM or YYYY-MM-DD
end   : ending of time, similar usage
type  : This is type of start-end input to use [D,W,M,Y]
        D - day   [YYYY-MM-DD] is preferrable
        W - Week  [YYYY-MM-DD] is preferrable
        M - Month [YYYY-MM] is preferrable
        Y - Year  [YYYY] is preferrable
size  : number of time series to be generated and inserted.
filename : a string in [filename.csv] this is an optional argument
'''
def random_walk(data, start_value=0, threshold=0.5, step_size=1, min_value=-np.inf, max_value=np.inf):
    previous_value = start_value
    for index, row in enumerate(data):
        if previous_value < min_value:
            previous_value = min_value
        if previous_value > max_value:
            previous_value = max_value
        probability = random.random()
        if probability >= threshold:
            data[index] = int(previous_value + step_size)
        else:
            data[index] = int(previous_value - step_size)
        previous_value = data[index]
    return data
file_name = None
if len(sys.argv) == 5:
    start = sys.argv[1]
    end = sys.argv[2]
    series_type = sys.argv[3]
    rows = int(sys.argv[4])
elif len(sys.argv) == 6:
    start = sys.argv[1]
    end = sys.argv[2]
    series_type = sys.argv[3]
    rows = int(sys.argv[4])
    file_name = sys.argv[5]
else:
    print("Wrong input")
    print("Usage : python create_time_series.py start end type size filename[Optional]")
    print("Example : python create_time_series.py '2020-01-01' '2020-12-31' 'D' 1000")

dates = np.arange(start, end, dtype='datetime64[{}]'.format(series_type))
dim = dates.size
columns = [str(date) for date in dates]
columns.insert(0,'Keys')
ts_sample = np.random.normal(-1,1,dim)
start_value = list(np.linspace(-200,200,400))
threshold_list = list(np.linspace(.3,.7,10))
step_size_list = list([-10,-5,-2,1,3,5,10])


data_values = []
for i in range(rows):
    value = list(random_walk(ts_sample, start_value=random.choice(start_value), threshold=random.choice(threshold_list), step_size=random.choice(step_size_list), min_value=random.choice(np.linspace(-200,50,250)), max_value=random.choice(np.linspace(-100,220,320))))
    value.insert(0, 'key_{}'.format(i))
    data_values.append(value)
dataset = pd.DataFrame(data_values,columns = columns)
if file_name == None:
    path = 'datasets//timeseries.csv'
else:
    path = os.path.join('datasets',file_name)

print("Your dataset path '{}'.".format(path))

dataset.to_csv(path, index=False)


