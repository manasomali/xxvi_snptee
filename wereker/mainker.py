# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 02:44:36 2021

@author: mathe
"""

import csv
import os
from prettytable import PrettyTable
from statistics import mean
from statistics import pstdev
from statistics import median
from natsort import natsorted
from ker import KER
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

bases=['original',
'agress0',
'agress1',
'agress2',
'agress3',
'et30',
'et35',
'et40',
'et45',
'et50',
'et55',
'sw03_w01',
'sw03_w02',
'sw03_w03',
'sw05_w01',
'sw05_w02',
'sw05_w03'
]
files=[]
for base in bases:
    if base=='original':
        files.append(str(base))
    else:
        files.append(str(base)+'_sr')
        #files.append(str(base)+'_nativo')

inputdirectory_np = os.path.dirname(os.path.realpath(__file__)) + '\\input\\naoprocessado'
inputdirectory_p = os.path.dirname(os.path.realpath(__file__)) + '\\input\\processado'

datasets_np={ file : [] for file in files }
datasets_p={ file : [] for file in files }

for file in files:
    new_file = csv.reader(open(inputdirectory_np+"/"+file+".csv", "r"),delimiter='_')
    new_file = natsorted(new_file)
    for row in list(new_file):
        datasets_np[file].append(row[4])
        
for file in files:
    new_file = csv.reader(open(inputdirectory_p+"/"+file+".csv", "r"),delimiter='_')
    new_file = natsorted(new_file)
    for row in list(new_file):
        datasets_p[file].append(row[1])

evaluations_np={ file : {} for file in files }
for file in files:
    keys = ['ker_mean','ker_median','ker_pstdev','ker_i']
    vals = [0, 0, 0, []]
    evaluations_np[file]=dict(zip(keys, vals))
         
evaluations_p={ file : {} for file in files }
for file in files:
    keys = ['ker_mean','ker_median','ker_pstdev','ker_i']
    vals = [0, 0, 0, []]
    evaluations_p[file]=dict(zip(keys, vals))
    

for dataset in datasets_np:
    for (orig,data)in zip(datasets_np['original'],datasets_np[dataset]):
        ker=KER(orig, data)
        evaluations_np[dataset]['ker_i'].append(ker.claculate())

for dataset in datasets_p:
    for (orig,data)in zip(datasets_p['original'],datasets_p[dataset]):
        ker=KER(orig, data)
        evaluations_p[dataset]['ker_i'].append(ker.claculate())
        
for dataset in datasets_np:
    evaluations_np[dataset]['ker_mean']=mean(evaluations_np[dataset]['ker_i'])
    evaluations_np[dataset]['ker_pstdev']=pstdev(evaluations_np[dataset]['ker_i'])
    evaluations_np[dataset]['ker_median']=median(evaluations_np[dataset]['ker_i'])

for dataset in datasets_p:
    evaluations_p[dataset]['ker_mean']=mean(evaluations_p[dataset]['ker_i'])
    evaluations_p[dataset]['ker_pstdev']=pstdev(evaluations_p[dataset]['ker_i'])
    evaluations_p[dataset]['ker_median']=median(evaluations_p[dataset]['ker_i'])

myTable = PrettyTable(['Set', 'mean KER', 'median KER', 'pstdev KER'])
for dataset in datasets_np:
    myTable.add_row([dataset.replace("_sr", "_np"),'{:.3f}'.format(evaluations_np[dataset]['ker_mean']),'{:.3f}'.format(evaluations_np[dataset]['ker_median']),'{:.3f}'.format(evaluations_np[dataset]['ker_pstdev'])])

for dataset in datasets_p:
    myTable.add_row([dataset.replace("_sr", "_p"),'{:.3f}'.format(evaluations_p[dataset]['ker_mean']),'{:.3f}'.format(evaluations_p[dataset]['ker_median']),'{:.3f}'.format(evaluations_p[dataset]['ker_pstdev'])])
   
print(myTable)

corpus = " ".join(datasets_p['original'])
ker=KER()
print("processado")
ker.generate_texto_wc(corpus)

#boxplot nao processados

vals = []
keys = []
for file in files:
    if file=='original':
        pass
    else:
        vals.append(evaluations_np[file]['ker_i'])
        keys.append(file)
    
my_dict = dict(zip(keys, vals))

fig, ax = plt.subplots(figsize=(10, 6))
meanlineprops = dict(linestyle='-', linewidth=1, color='blue')
flierprops = dict(marker='+', markerfacecolor='black')
ax.boxplot(my_dict.values(), meanprops=meanlineprops, meanline=True,showmeans=True,flierprops=flierprops)
fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
ax.set_xticklabels(my_dict.keys(),rotation=90)
legend_elements = [Line2D([0], [0], color='blue', lw=1, label='Média'),
                   Line2D([0], [0], color='orange', lw=1, label='Mediana')]
ax.legend(handles=legend_elements, loc='upper left')
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
ax.set_title('Boxplot')
ax.set_ylabel('KER')
ax.set_xlabel('Set')
plt.savefig('output\\boxplot1.tiff', format="tiff", dpi=300, bbox_inches='tight')

#boxplot processados

vals = []
keys = []
for file in files:
    if file=='original':
        pass
    else:
        vals.append(evaluations_p[file]['ker_i'])
        keys.append(file)
    
my_dict = dict(zip(keys, vals))

fig, ax = plt.subplots(figsize=(10, 6))
meanlineprops = dict(linestyle='-', linewidth=1, color='blue')
flierprops = dict(marker='+', markerfacecolor='black')
ax.boxplot(my_dict.values(), meanprops=meanlineprops, meanline=True,showmeans=True,flierprops=flierprops)
fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
ax.set_xticklabels(my_dict.keys(),rotation=90)
legend_elements = [Line2D([0], [0], color='blue', lw=1, label='Média'),
                   Line2D([0], [0], color='orange', lw=1, label='Mediana')]
ax.legend(handles=legend_elements, loc='upper left')
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
ax.set_title('Boxplot')
ax.set_ylabel('KER')
ax.set_xlabel('Set')
plt.savefig('output\\boxplot2.tiff', format="tiff", dpi=300, bbox_inches='tight')

#boxplot nao processados e processados

vals = []
keys = []
for file in files:
    if file=='original':
        pass
    else:
        vals.append(evaluations_np[file]['ker_i'])
        keys.append(file.replace("_sr", "_np"))
        vals.append(evaluations_p[file]['ker_i'])
        keys.append(file.replace("_sr", "_p"))
        
    
my_dict = dict(zip(keys, vals))

fig, ax = plt.subplots(figsize=(10, 6))
meanlineprops = dict(linestyle='-', linewidth=1, color='blue')
flierprops = dict(marker='+', markerfacecolor='black')
ax.boxplot(my_dict.values(), meanprops=meanlineprops, meanline=True,showmeans=True,flierprops=flierprops)
fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
ax.set_xticklabels(my_dict.keys(),rotation=90)
legend_elements = [Line2D([0], [0], color='blue', lw=1, label='Média'),
                   Line2D([0], [0], color='orange', lw=1, label='Mediana')]
ax.legend(handles=legend_elements, loc='upper left')
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
ax.set_title('Boxplot')
ax.set_ylabel('KER')
ax.set_xlabel('Set')
plt.savefig('output\\boxplot3.tiff', format="tiff", dpi=300, bbox_inches='tight')

# auditok

labels = [
'et30',
'et35',
'et40',
'et45',
'et50',
'et55',
]
dados_np=[]
for label in labels:
    dados_np.append(evaluations_np[str(label)+'_sr']['ker_mean'])

dados_p=[]
for label in labels:
    dados_p.append(evaluations_p[str(label)+'_sr']['ker_mean'])

labels = [
'30',
'35',
'40',
'45',
'50',
'55',
]
#nt=[]
#for label in labels:
#    nt.append(evaluations_p[str(label)+'_nativo']['wer_mean'])

x = np.arange(len(labels))
width = 0.2
gap = 0.05
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x + width*1.5, dados_np, width, label='Original')
g2=ax.barh(x + width/2, dados_p, width, label='Processado')
ax.set_yticks(x + width)
ax.set_xlim(right=0.45)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_title('auditok')
ax.set_ylabel('Energy Threshlod')
ax.set_xlabel('KER')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)
    
plt.savefig('output\\lib-auditok.tiff', format="tiff", dpi=300, bbox_inches='tight')

# pyAudioAnalysis

labels = [
'sw03_w01',
'sw03_w02',
'sw03_w03',
'sw05_w01',
'sw05_w02',
'sw05_w03'
]
dados_np=[]
for label in labels:
    dados_np.append(evaluations_np[str(label)+'_sr']['ker_mean'])

dados_p=[]
for label in labels:
    dados_p.append(evaluations_p[str(label)+'_sr']['ker_mean'])

labels = [
'0.3 | 0.1',
'0.3 | 0.2',
'0.3 | 0.3',
'0.5 | 0.1',
'0.5 | 0.2',
'0.5 | 0.3'
]

x = np.arange(len(labels))
width = 0.2
gap = 0.05
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x + width*1.5, dados_np, width, label='Original')
g2=ax.barh(x + width/2, dados_p, width, label='Processado')
ax.set_yticks(x + width)
ax.set_xlim(right=0.45)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_title('pyAudioAnalysis')
ax.set_ylabel('Smooth Window | Weight')
ax.set_xlabel('KER')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)
    
plt.savefig('output\\lib-pyAudioAnalysis.tiff', format="tiff", dpi=300, bbox_inches='tight')

# webrtcvad

labels = [
'agress0',
'agress1',
'agress2',
'agress3'
]
dados_np=[]
for label in labels:
    dados_np.append(evaluations_np[str(label)+'_sr']['ker_mean'])

dados_p=[]
for label in labels:
    dados_p.append(evaluations_p[str(label)+'_sr']['ker_mean'])

labels = [
'0',
'1',
'2',
'3'
]


x = np.arange(len(labels))
width = 0.2
gap = 0.05
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x + width*1.5, dados_np, width, label='Original')
g2=ax.barh(x + width/2, dados_p, width, label='Processado')
ax.set_yticks(x + width)
ax.set_xlim(right=0.45)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_title('webrtcvad')
ax.set_ylabel('Aggressiveness')
ax.set_xlabel('KER')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)
    
plt.savefig('output\\lib-webrtcvad.tiff', format="tiff", dpi=300, bbox_inches='tight')
