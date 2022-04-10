import pandas as pd

def clean_data(path='dataset/dataset.csv',final_column=''):
    dataset = pd.read_csv(path)
    columns = list(dataset.columns)
    idx = columns.index(final_column)
    dataset = dataset[columns[0:idx+1]]
    dataset.to_csv(path.replace(".csv", "_Final.csv"), index=False)

def get_min_max_attributes(table):
  min_attribute_values = list()
  max_attribute_values = list()
  for col in table.columns[1:]:
    min_attribute_values.append(table[col].min())
    max_attribute_values.append(table[col].max())
  return min_attribute_values,max_attribute_values