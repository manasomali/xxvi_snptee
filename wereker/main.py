# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 02:44:36 2021

@author: mathe
"""

import csv
import os
from prettytable import PrettyTable
import jiwer
from statistics import mean
from statistics import median
from statistics import pstdev
from natsort import natsorted
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from ker import KER
import pandas as pd
plt.rcParams.update({'font.size': 12})

def mk_groups(data):
    try:
        newdata = data.items()
    except:
        return

    thisgroup = []
    groups = []
    for key, value in newdata:
        newgroups = mk_groups(value)
        if newgroups is None:
            thisgroup.append((key, value))
        else:
            thisgroup.append((key, len(newgroups[-1])))
            if groups:
                groups = [g + n for n, g in zip(newgroups, groups)]
            else:
                groups = newgroups
    return [thisgroup] + groups

def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                      transform=ax.transAxes, color='black')
    line.set_clip_on(False)
    ax.add_line(line)

def label_group_bar(ax, data, color='tab:blue', alpha=1):
    groups = mk_groups(data)
    xy = groups.pop()
    x, y = zip(*xy)
    ly = len(y)
    xticks = range(1, ly + 1)
    
    ax.bar(xticks, y, align='center', width=0.9, color=color, alpha=alpha)
    ax.set_xticks(xticks)
    ax.set_xticklabels(x, weight='bold', fontsize=10)
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:.1}'.format(x) for x in vals], weight='bold', fontsize=14)
    ax.set_xlim(.5, ly + .5)
    ax.yaxis.grid(True)

    scale = 1. / ly
    for pos in range(ly + 1):  # change xrange to range for python3
        add_line(ax, pos * scale, -.1)
    ypos = -.2
    while groups:
        group = groups.pop()
        pos = 0
        for label, rpos in group:
            lxpos = (pos + .5 * rpos) * scale
            ax.text(lxpos, ypos, label, ha='center', transform=ax.transAxes, weight='bold')
            add_line(ax, pos * scale, ypos)
            pos += rpos
        add_line(ax, pos * scale, ypos)
        ypos -= .1



transformation = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemovePunctuation(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.SentencesToListOfWords(),
    jiwer.RemoveEmptyStrings()
])

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
    keys = ['wer_total', 'wer_mean','wer_median','wer_pstdev','wer_i', 'ker_mean','ker_median','ker_pstdev','ker_i']
    vals = [0, 0, 0, 0, [], 0, 0, 0, []]
    evaluations_np[file]=dict(zip(keys, vals))
    
evaluations_p={ file : {} for file in files }
for file in files:
    keys = ['wer_total', 'wer_mean','wer_median','wer_pstdev','wer_i', 'ker_mean','ker_median','ker_pstdev','ker_i']
    vals = [0, 0, 0, 0, [], 0, 0, 0, []]
    evaluations_p[file]=dict(zip(keys, vals))    

for evaluation in evaluations_np:
    evaluations_np[evaluation]['wer_total'] = jiwer.wer(datasets_np['original'], datasets_np[evaluation], truth_transform=transformation, hypothesis_transform=transformation)

for evaluation in evaluations_p:
    evaluations_p[evaluation]['wer_total'] = jiwer.wer(datasets_p['original'], datasets_p[evaluation], truth_transform=transformation, hypothesis_transform=transformation)


for dataset in datasets_np:
    for (orig,data)in zip(datasets_np['original'],datasets_np[dataset]):
        evaluations_np[dataset]['wer_i'].append(jiwer.wer(orig, data, truth_transform=transformation, hypothesis_transform=transformation))
        ker=KER(orig, data)
        evaluations_np[dataset]['ker_i'].append(ker.claculate())

for dataset in datasets_p:
    for (orig,data)in zip(datasets_p['original'],datasets_p[dataset]):
        evaluations_p[dataset]['wer_i'].append(jiwer.wer(orig, data, truth_transform=transformation, hypothesis_transform=transformation))
        ker=KER(orig, data)
        evaluations_p[dataset]['ker_i'].append(ker.claculate())

for dataset in datasets_np:
    evaluations_np[dataset]['wer_mean']=mean(evaluations_np[dataset]['wer_i'])
    evaluations_np[dataset]['wer_pstdev']=pstdev(evaluations_np[dataset]['wer_i'])
    evaluations_np[dataset]['wer_median']=median(evaluations_np[dataset]['wer_i'])
    evaluations_np[dataset]['ker_mean']=mean(evaluations_np[dataset]['ker_i'])
    evaluations_np[dataset]['ker_pstdev']=pstdev(evaluations_np[dataset]['ker_i'])
    evaluations_np[dataset]['ker_median']=median(evaluations_np[dataset]['ker_i'])

for dataset in datasets_p:
    evaluations_p[dataset]['wer_mean']=mean(evaluations_p[dataset]['wer_i'])
    evaluations_p[dataset]['wer_pstdev']=pstdev(evaluations_p[dataset]['wer_i'])
    evaluations_p[dataset]['wer_median']=median(evaluations_p[dataset]['wer_i'])
    evaluations_p[dataset]['ker_mean']=mean(evaluations_p[dataset]['ker_i'])
    evaluations_p[dataset]['ker_pstdev']=pstdev(evaluations_p[dataset]['ker_i'])
    evaluations_p[dataset]['ker_median']=median(evaluations_p[dataset]['ker_i'])

myTable = PrettyTable(['Set', 'mean WER', 'median WER', 'pstdev WER', 'mean KER', 'median KER', 'pstdev KER'])
for dataset in datasets_np:
    myTable.add_row([dataset.replace("_sr", "_np"),'{:.3f}'.format(evaluations_np[dataset]['wer_mean']),'{:.3f}'.format(evaluations_np[dataset]['wer_median']),'{:.3f}'.format(evaluations_np[dataset]['wer_pstdev']),'{:.3f}'.format(evaluations_np[dataset]['ker_mean']),'{:.3f}'.format(evaluations_np[dataset]['ker_median']),'{:.3f}'.format(evaluations_np[dataset]['ker_pstdev'])])

for dataset in datasets_p:
    myTable.add_row([dataset.replace("_sr", "_p"),'{:.3f}'.format(evaluations_p[dataset]['wer_mean']),'{:.3f}'.format(evaluations_p[dataset]['wer_median']),'{:.3f}'.format(evaluations_p[dataset]['wer_pstdev']),'{:.3f}'.format(evaluations_p[dataset]['ker_mean']),'{:.3f}'.format(evaluations_p[dataset]['ker_median']),'{:.3f}'.format(evaluations_p[dataset]['ker_pstdev'])])
   
print(myTable)

#boxplot nao processados wer

vals = []
keys = []
for file in files:
    if file=='original':
        pass
    else:
        vals.append(evaluations_np[file]['wer_i'])
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
ax.set_ylabel('WER')
ax.set_xlabel('Set')
plt.savefig('output\\boxplot nao processados wer.tiff', format="tiff", dpi=300, bbox_inches='tight')

#boxplot processados wer

vals = []
keys = []
for file in files:
    if file=='original':
        pass
    else:
        vals.append(evaluations_p[file]['wer_i'])
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
ax.set_ylabel('WER')
ax.set_xlabel('Set')
plt.savefig('output\\boxplot processados wer.tiff', format="tiff", dpi=300, bbox_inches='tight')

#boxplot nao processados e processados wer

vals = []
keys = []
for file in files:
    if file=='original':
        pass
    else:
        vals.append(evaluations_np[file]['wer_i'])
        keys.append(file.replace("_sr", "_np"))
        vals.append(evaluations_p[file]['wer_i'])
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
ax.set_ylabel('WER')
ax.set_xlabel('Set')
plt.savefig('output\\boxplot nao processados e processados wer.tiff', format="tiff", dpi=300, bbox_inches='tight')

# boxplot nao processados ker

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
plt.savefig('output\\boxplot nao processados ker.tiff', format="tiff", dpi=300, bbox_inches='tight')

#boxplot processados ker

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
plt.savefig('output\\boxplot processados ker.tiff', format="tiff", dpi=300, bbox_inches='tight')

#boxplot nao processados e processados ker

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
plt.savefig('output\\boxplot nao processados e processados ker.tiff', format="tiff", dpi=300, bbox_inches='tight')

# auditok webrtcvad pyAudioAnalysis ker wer
labels = [
'et30',
'et35',
'et40',
'et45',
'et50',
'et55',
'agress0',
'agress1',
'agress2',
'agress3',
'sw03_w01',
'sw03_w02',
'sw03_w03',
'sw05_w01',
'sw05_w02',
'sw05_w03'
]
dados_np_wer=[]
for label in labels:
    dados_np_wer.append(evaluations_np[str(label)+'_sr']['wer_mean'])
dados_np_ker=[]
for label in labels:
    dados_np_ker.append(evaluations_np[str(label)+'_sr']['ker_mean'])

labels = [
'Energy Threshlod: 30',
'Energy Threshlod: 35',
'Energy Threshlod: 40',
'Energy Threshlod: 45',
'Energy Threshlod: 50',
'Energy Threshlod: 55',
'Aggressiveness: 0',
'Aggressiveness: 1',
'Aggressiveness: 2',
'Aggressiveness: 3',
'Smooth Window: 0.3 | Weight: 0.1',
'Smooth Window: 0.3 | Weight: 0.2',
'Smooth Window: 0.3 | Weight: 0.3',
'Smooth Window: 0.5 | Weight: 0.1',
'Smooth Window: 0.5 | Weight: 0.2',
'Smooth Window: 0.5 | Weight: 0.3'
]
x = np.arange(len(labels))
width = 0.45
fig, ax = plt.subplots(figsize=(12, 10))
g1=ax.barh(x + width*1.5, dados_np_wer, width, label='WER')
g2=ax.barh(x + width/2, dados_np_ker, width, label='KER')
ax.set_yticks(x + width)
ax.set_xlim(right=0.65)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_ylabel('Parâmetros')
ax.set_xlabel('Métrica')
plt.grid(axis = 'x')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container,fmt='%.4g',padding=-40)
    
plt.savefig('output\\auditok webrtcvad pyAudioAnalysis ker wer.tiff', format="tiff", dpi=300, bbox_inches='tight')

# geral wer np

data = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_np['et30_sr']['wer_mean'],
            '35': evaluations_np['et35_sr']['wer_mean'],
            '40': evaluations_np['et40_sr']['wer_mean'],
            '45': evaluations_np['et45_sr']['wer_mean'],
            '50': evaluations_np['et50_sr']['wer_mean'],
            '55': evaluations_np['et55_sr']['wer_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_np['agress0_sr']['wer_mean'],
            '1': evaluations_np['agress1_sr']['wer_mean'],
            '2': evaluations_np['agress2_sr']['wer_mean'],
            '3': evaluations_np['agress3_sr']['wer_mean']
        }
    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_np['sw03_w01_sr']['wer_mean'],
            '0.3|0.2': evaluations_np['sw03_w02_sr']['wer_mean'],
            '0.3|0.3': evaluations_np['sw03_w03_sr']['wer_mean'],
            '0.5|0.1': evaluations_np['sw05_w01_sr']['wer_mean'],
            '0.5|0.2': evaluations_np['sw05_w03_sr']['wer_mean'],
            '0.5|0.3': evaluations_np['sw05_w03_sr']['wer_mean']
        }
    }
}
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('WER')
ax.set_ylim(top=0.6)
label_group_bar(ax, data)
fig.subplots_adjust(bottom=0.3)
for container in ax.containers:
    ax.bar_label(container,fmt='%.3g',padding=0)

plt.savefig('output\\auditok webrtcvad pyAudioAnalysis wer.tiff', format="tiff", dpi=300, bbox_inches='tight')

# geral ker np


data = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_np['et30_sr']['ker_mean'],
            '35': evaluations_np['et35_sr']['ker_mean'],
            '40': evaluations_np['et40_sr']['ker_mean'],
            '45': evaluations_np['et45_sr']['ker_mean'],
            '50': evaluations_np['et50_sr']['ker_mean'],
            '55': evaluations_np['et55_sr']['ker_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_np['agress0_sr']['ker_mean'],
            '1': evaluations_np['agress1_sr']['ker_mean'],
            '2': evaluations_np['agress2_sr']['ker_mean'],
            '3': evaluations_np['agress3_sr']['ker_mean']
        }
    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_np['sw03_w01_sr']['ker_mean'],
            '0.3|0.2': evaluations_np['sw03_w02_sr']['ker_mean'],
            '0.3|0.3': evaluations_np['sw03_w03_sr']['ker_mean'],
            '0.5|0.1': evaluations_np['sw05_w01_sr']['ker_mean'],
            '0.5|0.2': evaluations_np['sw05_w03_sr']['ker_mean'],
            '0.5|0.3': evaluations_np['sw05_w03_sr']['ker_mean']
        }
    }
}
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('KER')
ax.set_ylim(top=0.6)
label_group_bar(ax, data)
fig.subplots_adjust(bottom=0.3)
for container in ax.containers:
    ax.bar_label(container,fmt='%.3g',padding=0)

plt.savefig('output\\auditok webrtcvad pyAudioAnalysis ker.tiff', format="tiff", dpi=300, bbox_inches='tight')


ker_p = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_p['et30_sr']['ker_mean'],
            '35': evaluations_p['et35_sr']['ker_mean'],
            '40': evaluations_p['et40_sr']['ker_mean'],
            '45': evaluations_p['et45_sr']['ker_mean'],
            '50': evaluations_p['et50_sr']['ker_mean'],
            '55': evaluations_p['et55_sr']['ker_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_p['agress0_sr']['ker_mean'],
            '1': evaluations_p['agress1_sr']['ker_mean'],
            '2': evaluations_p['agress2_sr']['ker_mean'],
            '3': evaluations_p['agress3_sr']['ker_mean']
        }    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_p['sw03_w01_sr']['ker_mean'],
            '0.3|0.2': evaluations_p['sw03_w02_sr']['ker_mean'],
            '0.3|0.3': evaluations_p['sw03_w03_sr']['ker_mean'],
            '0.5|0.1': evaluations_p['sw05_w01_sr']['ker_mean'],
            '0.5|0.2': evaluations_p['sw05_w03_sr']['ker_mean'],
            '0.5|0.3': evaluations_p['sw05_w03_sr']['ker_mean']
        }
    }
}
ker_np = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_np['et30_sr']['ker_mean'],
            '35': evaluations_np['et35_sr']['ker_mean'],
            '40': evaluations_np['et40_sr']['ker_mean'],
            '45': evaluations_np['et45_sr']['ker_mean'],
            '50': evaluations_np['et50_sr']['ker_mean'],
            '55': evaluations_np['et55_sr']['ker_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_np['agress0_sr']['ker_mean'],
            '1': evaluations_np['agress1_sr']['ker_mean'],
            '2': evaluations_np['agress2_sr']['ker_mean'],
            '3': evaluations_np['agress3_sr']['ker_mean']
        }    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_np['sw03_w01_sr']['ker_mean'],
            '0.3|0.2': evaluations_np['sw03_w02_sr']['ker_mean'],
            '0.3|0.3': evaluations_np['sw03_w03_sr']['ker_mean'],
            '0.5|0.1': evaluations_np['sw05_w01_sr']['ker_mean'],
            '0.5|0.2': evaluations_np['sw05_w03_sr']['ker_mean'],
            '0.5|0.3': evaluations_np['sw05_w03_sr']['ker_mean']
        }
    }
}
wer_p = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_p['et30_sr']['wer_mean'],
            '35': evaluations_p['et35_sr']['wer_mean'],
            '40': evaluations_p['et40_sr']['wer_mean'],
            '45': evaluations_p['et45_sr']['wer_mean'],
            '50': evaluations_p['et50_sr']['wer_mean'],
            '55': evaluations_p['et55_sr']['wer_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_p['agress0_sr']['wer_mean'],
            '1': evaluations_p['agress1_sr']['wer_mean'],
            '2': evaluations_p['agress2_sr']['wer_mean'],
            '3': evaluations_p['agress3_sr']['wer_mean']
        }    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_p['sw03_w01_sr']['wer_mean'],
            '0.3|0.2': evaluations_p['sw03_w02_sr']['wer_mean'],
            '0.3|0.3': evaluations_p['sw03_w03_sr']['wer_mean'],
            '0.5|0.1': evaluations_p['sw05_w01_sr']['wer_mean'],
            '0.5|0.2': evaluations_p['sw05_w03_sr']['wer_mean'],
            '0.5|0.3': evaluations_p['sw05_w03_sr']['wer_mean']
        }
    }
}
wer_np = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_np['et30_sr']['wer_mean'],
            '35': evaluations_np['et35_sr']['wer_mean'],
            '40': evaluations_np['et40_sr']['wer_mean'],
            '45': evaluations_np['et45_sr']['wer_mean'],
            '50': evaluations_np['et50_sr']['wer_mean'],
            '55': evaluations_np['et55_sr']['wer_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_np['agress0_sr']['wer_mean'],
            '1': evaluations_np['agress1_sr']['wer_mean'],
            '2': evaluations_np['agress2_sr']['wer_mean'],
            '3': evaluations_np['agress3_sr']['wer_mean']
        }    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_np['sw03_w01_sr']['wer_mean'],
            '0.3|0.2': evaluations_np['sw03_w02_sr']['wer_mean'],
            '0.3|0.3': evaluations_np['sw03_w03_sr']['wer_mean'],
            '0.5|0.1': evaluations_np['sw05_w01_sr']['wer_mean'],
            '0.5|0.2': evaluations_np['sw05_w03_sr']['wer_mean'],
            '0.5|0.3': evaluations_np['sw05_w03_sr']['wer_mean']
        }
    }
}

libs=['auditok','webrtcvad','pyAudioAnalysis']
wer_np_vec=[]
for lib in libs:
    for dado1 in wer_np[lib]:
        for dado2 in wer_np[lib][dado1]:
            wer_np_vec.append(wer_np[lib][dado1][dado2])
            
wer_p_vec=[]
for lib in libs:
    for dado1 in wer_p[lib]:
        for dado2 in wer_p[lib][dado1]:
            wer_p_vec.append(wer_p[lib][dado1][dado2])
            
reducao_wer=[]          
for (wernp, werp) in zip(wer_np_vec,wer_p_vec):
    reducao_wer.append(100-(werp*100/wernp))

ker_np_vec=[]
for lib in libs:
    for dado1 in ker_np[lib]:
        for dado2 in ker_np[lib][dado1]:
            ker_np_vec.append(ker_np[lib][dado1][dado2])
            
ker_p_vec=[]
for lib in libs:
    for dado1 in ker_p[lib]:
        for dado2 in ker_p[lib][dado1]:
            ker_p_vec.append(ker_p[lib][dado1][dado2])
            
reducao_ker=[]
for (kernp, kerp) in zip(ker_np_vec,ker_p_vec):
    reducao_ker.append(100-(kerp*100/kernp))
    


# geral wer p
data = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_p['et30_sr']['wer_mean'],
            '35': evaluations_p['et35_sr']['wer_mean'],
            '40': evaluations_p['et40_sr']['wer_mean'],
            '45': evaluations_p['et45_sr']['wer_mean'],
            '50': evaluations_p['et50_sr']['wer_mean'],
            '55': evaluations_p['et55_sr']['wer_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_p['agress0_sr']['wer_mean'],
            '1': evaluations_p['agress1_sr']['wer_mean'],
            '2': evaluations_p['agress2_sr']['wer_mean'],
            '3': evaluations_p['agress3_sr']['wer_mean']
        }
    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_p['sw03_w01_sr']['wer_mean'],
            '0.3|0.2': evaluations_p['sw03_w02_sr']['wer_mean'],
            '0.3|0.3': evaluations_p['sw03_w03_sr']['wer_mean'],
            '0.5|0.1': evaluations_p['sw05_w01_sr']['wer_mean'],
            '0.5|0.2': evaluations_p['sw05_w03_sr']['wer_mean'],
            '0.5|0.3': evaluations_p['sw05_w03_sr']['wer_mean']
        }
    }
}
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('WER', fontsize=16, weight='bold')
ax.set_ylim(top=0.65)
label_group_bar(ax, wer_np, color='tab:blue', alpha=0.5)
label_group_bar(ax, data, color='tab:orange')
cont=0
for p in ax.patches:
    ax.annotate("-"+'{0:.1f}'.format(reducao_wer[cont])+"%", (p.get_x() * 1.005, 0.01), weight='bold', fontsize=11)
    if cont==15:
        break
    
    cont+=1
    
fig.subplots_adjust(bottom=0.3)
for container in ax.containers:
    ax.bar_label(container,fmt='%.3g',padding=0)


plt.savefig('output\\auditok webrtcvad pyAudioAnalysis wer p.tiff', format="tiff", dpi=300, bbox_inches='tight')

# geral ker p


data = {
    'auditok': {
        'Energy Threshlod': {
            '30': evaluations_p['et30_sr']['ker_mean'],
            '35': evaluations_p['et35_sr']['ker_mean'],
            '40': evaluations_p['et40_sr']['ker_mean'],
            '45': evaluations_p['et45_sr']['ker_mean'],
            '50': evaluations_p['et50_sr']['ker_mean'],
            '55': evaluations_p['et55_sr']['ker_mean']
        }
    },
    'webrtcvad': {
        'Aggressiveness': {
            '0': evaluations_p['agress0_sr']['ker_mean'],
            '1': evaluations_p['agress1_sr']['ker_mean'],
            '2': evaluations_p['agress2_sr']['ker_mean'],
            '3': evaluations_p['agress3_sr']['ker_mean']
        }    },
    'pyAudioAnalysis': {
        'Smooth Window|Weight': {
            '0.3|0.1': evaluations_p['sw03_w01_sr']['ker_mean'],
            '0.3|0.2': evaluations_p['sw03_w02_sr']['ker_mean'],
            '0.3|0.3': evaluations_p['sw03_w03_sr']['ker_mean'],
            '0.5|0.1': evaluations_p['sw05_w01_sr']['ker_mean'],
            '0.5|0.2': evaluations_p['sw05_w03_sr']['ker_mean'],
            '0.5|0.3': evaluations_p['sw05_w03_sr']['ker_mean']
        }
    }
}
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('KER', fontsize=16, weight='bold')
ax.set_ylim(top=0.65)
label_group_bar(ax, ker_np, color='tab:blue', alpha=0.5)
label_group_bar(ax, data, color='tab:orange')

cont=0
for p in ax.patches:
    ax.annotate("-"+'{0:.1f}'.format(reducao_ker[cont])+"%", (p.get_x() * 1.005, 0.01), weight='bold', fontsize=11)
    if cont==15:
        break
    
    cont+=1
    
fig.subplots_adjust(bottom=0.3)
for container in ax.containers:
    ax.bar_label(container,fmt='%.3g',padding=0)

plt.savefig('output\\auditok webrtcvad pyAudioAnalysis ker p.tiff', format="tiff", dpi=300, bbox_inches='tight')

# auditok

labels = [
'et30',
'et35',
'et40',
'et45',
'et50',
'et55',
]
dados_np_wer=[]
for label in labels:
    dados_np_wer.append(evaluations_np[str(label)+'_sr']['wer_mean'])
dados_np_ker=[]
for label in labels:
    dados_np_ker.append(evaluations_np[str(label)+'_sr']['ker_mean'])

labels = [
'30',
'35',
'40',
'45',
'50',
'55'
]
#nt=[]
#for label in labels:
#    nt.append(evaluations_p[str(label)+'_nativo']['wer_mean'])

x = np.arange(len(labels))
width = 0.2
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x + width*1.5, dados_np_wer, width, label='WER')
g2=ax.barh(x + width/2, dados_np_ker, width, label='KER')
ax.set_yticks(x + width)
ax.set_xlim(right=0.65)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_title('auditok')
ax.set_ylabel('Energy Threshlod')
ax.set_xlabel('WER')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)
    
plt.savefig('output\\auditok.tiff', format="tiff", dpi=300, bbox_inches='tight')

# pyAudioAnalysis

labels = [
'sw03_w01',
'sw03_w02',
'sw03_w03',
'sw05_w01',
'sw05_w02',
'sw05_w03'
]
dados_np_wer=[]
for label in labels:
    dados_np_wer.append(evaluations_np[str(label)+'_sr']['wer_mean'])
dados_np_ker=[]
for label in labels:
    dados_np_ker.append(evaluations_np[str(label)+'_sr']['ker_mean'])

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
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x + width*1.5, dados_np_wer, width, label='WER')
g2=ax.barh(x + width/2, dados_np_ker, width, label='KER')
ax.set_yticks(x + width)
ax.set_xlim(right=0.65)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_title('pyAudioAnalysis')
ax.set_ylabel('Smooth Window | Weight')
ax.set_xlabel('WER')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)
    
plt.savefig('output\\pyAudioAnalysis.tiff', format="tiff", dpi=300, bbox_inches='tight')

# webrtcvad

labels = [
'agress0',
'agress1',
'agress2',
'agress3'
]
dados_np_wer=[]
for label in labels:
    dados_np_wer.append(evaluations_np[str(label)+'_sr']['wer_mean'])
dados_np_ker=[]
for label in labels:
    dados_np_ker.append(evaluations_np[str(label)+'_sr']['ker_mean'])

labels = [
'0',
'1',
'2',
'3'
]


x = np.arange(len(labels))
width = 0.2
fig, ax = plt.subplots(figsize=(10, 6))
g1=ax.barh(x + width*1.5, dados_np_wer, width, label='WER')
g2=ax.barh(x + width/2, dados_np_ker, width, label='KER')
ax.set_yticks(x + width)
ax.set_xlim(right=0.65)
ax.set_yticklabels(labels)
ax.legend(loc='upper left')
ax.set_title('webrtcvad')
ax.set_ylabel('Aggressiveness')
ax.set_xlabel('WER')
ax.set_ylim=[2*width - 1, len(labels)]
for container in ax.containers:
    ax.bar_label(container)
    
plt.savefig('output\\webrtcvad.tiff', format="tiff", dpi=300, bbox_inches='tight')


