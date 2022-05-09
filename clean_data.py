import sys
import pandas as pd
import os

if len(sys.argv) == 4:
    input_path = sys.argv[1]
    num_columns = int(sys.argv[2])
    num_rows = int(sys.argv[3])
    
    try:
        dataset = pd.read_csv(input_path)
    except PermissionError:
        print(' Usage: Specify correct path and make sure the file is CSV.')
    columns = dataset.columns[:num_columns]
    dataset = dataset[columns]
    dataset = dataset.head(num_rows)
    dataset.fillna(0,inplace=True)
    
    file_name = input_path.split('\\')[-1].split('.')
    new_file_name = '{}_cleaned.{}'.format(file_name[0],file_name[1])
    path = os.path.join('datasets',new_file_name)
    print('use {} as path'.format(path))
    dataset.to_csv(path, index=False)
    
else:
    print(' Usage: python clean_data.py path number_of_columns_to_be_selected number_of_rows_to_be_selected')