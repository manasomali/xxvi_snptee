# -*- coding: utf-8 -*-
import csv
import os
from prettytable import PrettyTable
from statistics import mean
from statistics import pstdev
from natsort import natsorted
from ker import KER
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def printdic(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            printdic(value, indent+1)
        else:
            if isinstance(value, float):
                print('\t' * (indent+1) + str(value))

files=['original',
    'semsilencio3_separado0_agrupados',
    'semsilencio3_separado0ponto1_agrupados',
    'semsilencio3_separado0ponto2_agrupados',
    'separado0_agrupados',
    'separado0ponto1_agrupados',
    'separado0ponto2_agrupados',
    'semsilencio0_separado0_agrupados',
    'semsilencio0_separado0ponto1_agrupados',
    'semsilencio0_separado0ponto2_agrupados',
    'semsilencio0_separado0ponto1_somenteinicio_agrupados',
    'semsilencio0_separado0ponto2_somenteinicio_agrupados']

inputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\input'

datasets={'original':[],
    'semsilencio3_separado0_agrupados':[],
    'semsilencio3_separado0ponto1_agrupados':[],
    'semsilencio3_separado0ponto2_agrupados':[],
    'separado0_agrupados':[],
    'separado0ponto1_agrupados':[],
    'separado0ponto2_agrupados':[],
    'semsilencio0_separado0_agrupados':[],
    'semsilencio0_separado0ponto1_agrupados':[],
    'semsilencio0_separado0ponto2_agrupados':[],
    'semsilencio0_separado0ponto1_somenteinicio_agrupados':[],
    'semsilencio0_separado0ponto2_somenteinicio_agrupados':[]}

for file in files:
    new_file = csv.reader(open(inputdirectory+"/"+file+".csv", "r"),delimiter='_')
    new_file = natsorted(new_file)
    for row in list(new_file):
        datasets[file].append(row[1])
        
evaluations={
    'semsilencio3_separado0_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio3_separado0ponto1_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio3_separado0ponto2_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'separado0_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'separado0ponto1_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'separado0ponto2_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio0_separado0_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio0_separado0ponto1_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio0_separado0ponto2_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio0_separado0ponto1_somenteinicio_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},
    'semsilencio0_separado0ponto2_somenteinicio_agrupados':{'ker_mean':0,'ker_pstdev':0,'ker_i':[]},}

for evaluation in evaluations:
    corpus_ori = " ".join(datasets['original'])
    corpus_eval = " ".join(datasets[evaluation])
    ker=KER(corpus_ori, corpus_eval)
    evaluations[evaluation]['ker_total'] = ker.claculate()
    
for (orig,s3s0,s3s01,s3s02,s0,s01,s02,s0s0,s0s01,s0s02,s0s01_si,s0s02_si) in zip(datasets['original'],
                                           datasets['semsilencio3_separado0_agrupados'],
                                           datasets['semsilencio3_separado0ponto1_agrupados'],
                                           datasets['semsilencio3_separado0ponto2_agrupados'],
                                           datasets['separado0_agrupados'],
                                           datasets['separado0ponto1_agrupados'],
                                           datasets['separado0ponto2_agrupados'],
                                           datasets['semsilencio0_separado0_agrupados'],
                                           datasets['semsilencio0_separado0ponto1_agrupados'],
                                           datasets['semsilencio0_separado0ponto2_agrupados'],
                                           datasets['semsilencio0_separado0ponto1_somenteinicio_agrupados'],
                                           datasets['semsilencio0_separado0ponto2_somenteinicio_agrupados']):
    ker=KER(orig, s3s0)
    evaluations['semsilencio3_separado0_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s3s01)
    evaluations['semsilencio3_separado0ponto1_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s3s02)
    evaluations['semsilencio3_separado0ponto2_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s0)
    evaluations['separado0_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s01)
    evaluations['separado0ponto1_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s02)
    evaluations['separado0ponto2_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s0s0)
    evaluations['semsilencio0_separado0_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s0s01)
    evaluations['semsilencio0_separado0ponto1_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s0s02)
    evaluations['semsilencio0_separado0ponto2_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s0s01_si)
    evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_i'].append(ker.claculate())
    ker=KER(orig, s0s02_si)
    evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_i'].append(ker.claculate())
    

evaluations['semsilencio3_separado0_agrupados']['ker_mean'] = mean(evaluations['semsilencio3_separado0_agrupados']['ker_i'])
evaluations['semsilencio3_separado0_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio3_separado0_agrupados']['ker_i'])

evaluations['semsilencio3_separado0ponto1_agrupados']['ker_mean'] = mean(evaluations['semsilencio3_separado0ponto1_agrupados']['ker_i'])
evaluations['semsilencio3_separado0ponto1_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio3_separado0ponto1_agrupados']['ker_i'])

evaluations['semsilencio3_separado0ponto2_agrupados']['ker_mean'] = mean(evaluations['semsilencio3_separado0ponto2_agrupados']['ker_i'])
evaluations['semsilencio3_separado0ponto2_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio3_separado0ponto2_agrupados']['ker_i'])

evaluations['separado0_agrupados']['ker_mean'] = mean(evaluations['separado0_agrupados']['ker_i'])
evaluations['separado0_agrupados']['ker_pstdev'] = pstdev(evaluations['separado0_agrupados']['ker_i'])

evaluations['separado0ponto1_agrupados']['ker_mean'] = mean(evaluations['separado0ponto1_agrupados']['ker_i'])
evaluations['separado0ponto1_agrupados']['ker_pstdev'] = pstdev(evaluations['separado0ponto1_agrupados']['ker_i'])

evaluations['separado0ponto2_agrupados']['ker_mean'] = mean(evaluations['separado0ponto2_agrupados']['ker_i'])
evaluations['separado0ponto2_agrupados']['ker_pstdev'] = pstdev(evaluations['separado0ponto2_agrupados']['ker_i'])

evaluations['semsilencio0_separado0_agrupados']['ker_mean'] = mean(evaluations['semsilencio0_separado0_agrupados']['ker_i'])
evaluations['semsilencio0_separado0_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio0_separado0_agrupados']['ker_i'])


evaluations['semsilencio0_separado0ponto1_agrupados']['ker_mean'] = mean(evaluations['semsilencio0_separado0ponto1_agrupados']['ker_i'])
evaluations['semsilencio0_separado0ponto1_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio0_separado0ponto1_agrupados']['ker_i'])

evaluations['semsilencio0_separado0ponto2_agrupados']['ker_mean'] = mean(evaluations['semsilencio0_separado0ponto2_agrupados']['ker_i'])
evaluations['semsilencio0_separado0ponto2_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio0_separado0ponto2_agrupados']['ker_i'])

evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_mean'] = mean(evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_i'])
evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_i'])

evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_mean'] = mean(evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_i'])
evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_pstdev'] = pstdev(evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_i'])

printdic(evaluations)
myTable = PrettyTable(['Set', 'mean ker', 'pstdev ker'])
myTable.add_row(['semsilencio3_separado0_agrupados','{:.3f}'.format(evaluations['semsilencio3_separado0_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio3_separado0_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio3_separado0ponto1_agrupados','{:.3f}'.format(evaluations['semsilencio3_separado0ponto1_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio3_separado0ponto1_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio3_separado0ponto2_agrupados','{:.3f}'.format(evaluations['semsilencio3_separado0ponto2_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio3_separado0ponto2_agrupados']['ker_pstdev'])])
myTable.add_row(['separado0_agrupados','{:.3f}'.format(evaluations['separado0_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['separado0_agrupados']['ker_pstdev'])])
myTable.add_row(['separado0ponto1_agrupados','{:.3f}'.format(evaluations['separado0ponto1_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['separado0ponto1_agrupados']['ker_pstdev'])])
myTable.add_row(['separado0ponto2_agrupados','{:.3f}'.format(evaluations['separado0ponto2_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['separado0ponto2_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio0_separado0_agrupados','{:.3f}'.format(evaluations['semsilencio0_separado0_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio0_separado0_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio0_separado0ponto1_agrupados','{:.3f}'.format(evaluations['semsilencio0_separado0ponto1_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio0_separado0ponto1_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio0_separado0ponto2_agrupados','{:.3f}'.format(evaluations['semsilencio0_separado0ponto2_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio0_separado0ponto2_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio0_separado0ponto1_somenteinicio_agrupados','{:.3f}'.format(evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_pstdev'])])
myTable.add_row(['semsilencio0_separado0ponto2_somenteinicio_agrupados','{:.3f}'.format(evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_mean']),'{:.3f}'.format(evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_pstdev'])])
print(myTable)

corpus = " ".join(datasets['original'])
ker=KER()
ker.generate_texto_wc(corpus)

my_dict = {'semsilencio0 separado0': evaluations['semsilencio0_separado0_agrupados']['ker_i'],
           'semsilencio0 separado0ponto1': evaluations['semsilencio0_separado0ponto1_agrupados']['ker_i'],
           'semsilencio0 separado0ponto2': evaluations['semsilencio0_separado0ponto2_agrupados']['ker_i'],
           'semsilencio0 separado0ponto1 somenteinicio': evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_i'],
           'semsilencio0 separado0ponto2 somenteinicio': evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_i'],
           'semsilencio3 separado0': evaluations['semsilencio3_separado0_agrupados']['ker_i'],
           'semsilencio3 separado0ponto1': evaluations['semsilencio3_separado0ponto1_agrupados']['ker_i'],
           'semsilencio3 separado0ponto2': evaluations['semsilencio3_separado0ponto2_agrupados']['ker_i'],
           'separado0': evaluations['separado0_agrupados']['ker_i'],
           'separado0ponto1': evaluations['separado0ponto1_agrupados']['ker_i'],
           'separado0ponto2': evaluations['separado0ponto2_agrupados']['ker_i']}

fig, ax = plt.subplots(figsize=(10, 6))
meanlineprops = dict(linestyle='-', linewidth=1, color='blue')
flierprops = dict(marker='+', markerfacecolor='black')
ax.boxplot(my_dict.values(), meanprops=meanlineprops, meanline=True,showmeans=True,flierprops=flierprops)
fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
ax.set_xticklabels(my_dict.keys(),rotation=90)
legend_elements = [Line2D([0], [0], color='blue', lw=1, label='Média'),
                   Line2D([0], [0], color='orange', lw=1, label='Mediana')]
ax.legend(handles=legend_elements, loc='upper right')
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)


labels = ['semsilencio0 separado0',
          'semsilencio0 separado0ponto1',
          'semsilencio0 separado0ponto2',
          'semsilencio0 separado0ponto1 somenteinicio',
          'semsilencio0 separado0ponto2 somenteinicio',
          'semsilencio3 separado0',
          'semsilencio3 separado0ponto1',
          'semsilencio3 separado0ponto2',
          'separado0',
          'separado0ponto1',
          'separado0ponto2']

means = [evaluations['semsilencio0_separado0_agrupados']['ker_mean'],
           evaluations['semsilencio0_separado0ponto1_agrupados']['ker_mean'],
           evaluations['semsilencio0_separado0ponto2_agrupados']['ker_mean'],
           evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_mean'],
           evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_mean'],
           evaluations['semsilencio3_separado0_agrupados']['ker_mean'],
           evaluations['semsilencio3_separado0ponto1_agrupados']['ker_mean'],
           evaluations['semsilencio3_separado0ponto2_agrupados']['ker_mean'],
           evaluations['separado0_agrupados']['ker_mean'],
           evaluations['separado0ponto1_agrupados']['ker_mean'],
           evaluations['separado0ponto2_agrupados']['ker_mean']]

dvp = [evaluations['semsilencio0_separado0_agrupados']['ker_pstdev'],
           evaluations['semsilencio0_separado0ponto1_agrupados']['ker_pstdev'],
           evaluations['semsilencio0_separado0ponto2_agrupados']['ker_pstdev'],
           evaluations['semsilencio0_separado0ponto1_somenteinicio_agrupados']['ker_pstdev'],
           evaluations['semsilencio0_separado0ponto2_somenteinicio_agrupados']['ker_pstdev'],
           evaluations['semsilencio3_separado0_agrupados']['ker_pstdev'],
           evaluations['semsilencio3_separado0ponto1_agrupados']['ker_pstdev'],
           evaluations['semsilencio3_separado0ponto2_agrupados']['ker_pstdev'],
           evaluations['separado0_agrupados']['ker_pstdev'],
           evaluations['separado0ponto1_agrupados']['ker_pstdev'],
           evaluations['separado0ponto2_agrupados']['ker_pstdev']]

x = np.arange(len(means))
width = 0.3
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x, means, width, label='Média')
g2=ax.barh(x + width, dvp, width, label='Desvio Padrão')
ax.set_yticks(x + width)
ax.set_xlim(right=0.35)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)


    