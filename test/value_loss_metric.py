import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def find_value_loss(dataset):
    columns = dataset.columns[1:len(dataset.columns)-2]
    total_loss = 0
    for column in columns:
        Q = list(dataset[column])
        value_loss_Q = 0
        for value in Q:
            value = value[1:-1].split('-')
            if len(value)==2:
                lower = int(float(value[0]))
                upper = int(float(value[1]))
            elif len(value)==3:
                if len(value[0])==0:
                    lower = int(float('-'+value[1]))
                    upper = int(float(value[2]))
                else:
                    lower = int(float(value[0]))
                    upper = int(float('-'+value[2]))
            else:
                lower = int(float('-'+value[1]))
                upper = int(float('-'+value[3]))
            value_loss_Q = value_loss_Q + pow(upper-lower,2)
        value_loss_Q = value_loss_Q/len(Q)
        value_loss_Q = np.sqrt(value_loss_Q)
        total_loss = total_loss+value_loss_Q
    
    return total_loss

def plot_barchart(x_axis, data, label):

    kapra = list()
    naive = list()
    x = list()
    list_idx = np.argsort(x_axis)
    for idx in list_idx:
        x.append(x_axis[idx])
        naive.append(data['naive'][idx])
        kapra.append(data['kapra'][idx])
    barWidth = 0.25
    
    naive_bar = np.arange(len(naive))
    kapra_bar = [x + barWidth for x in naive_bar]
    fig = plt.figure(figsize =(12, 8))
    plt.bar(naive_bar, naive, color ='r', width = barWidth, edgecolor ='red', label ='Naive Algorithm')
    plt.bar(kapra_bar, kapra, color ='b', width = barWidth, edgecolor ='blue', label ='Kapra Algorithm')
    plt.xlabel(label, fontweight ='bold', fontsize = 10)
    plt.ylabel('Value loss', fontweight ='bold', fontsize = 10)
    plt.xticks([r + barWidth/2 for r in range(len(naive))], x)
    plt.legend()
    plt.savefig('figures\\bar_plot_vl_{}.png'.format(label))



folder_names = ["k_values", "p_values"]

x_label_k = list()
x_label_p = list()
value_loss_k = {"naive":[],"kapra":[]}
value_loss_p = {"naive":[],"kapra":[]}

for file in os.listdir('output'):
    if file in folder_names:
        path = os.path.join('output',file)
        for inner_file in os.listdir(path):
            output_file = os.path.join(path,inner_file)
            anonymized = pd.read_csv(output_file)
            info = inner_file.split('_')
            if info[1] == 'k':                
                if info[2]=='kapra':
                  x_label_k.append(int(info[3].split('.')[0]))
                  value_loss_k['kapra'].append(find_value_loss(anonymized))
                elif info[2]=='naive':
                  value_loss_k['naive'].append(find_value_loss(anonymized))
            elif info[1] == 'p':                
                if info[2]=='kapra':
                  x_label_p.append(int(info[3].split('.')[0]))
                  value_loss_p['kapra'].append(find_value_loss(anonymized))
                elif info[2]=='naive':
                  value_loss_p['naive'].append(find_value_loss(anonymized))

plot_barchart(x_label_k, value_loss_k, "K value")
plot_barchart(x_label_p, value_loss_p, "P value")
      




