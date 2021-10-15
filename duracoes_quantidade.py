# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 19:40:43 2021

@author: mathe
"""

from prettytable import PrettyTable
from scipy.io.wavfile import read
import os
from tqdm import tqdm
from tkinter import Tk
from tkinter import filedialog
import re
from statistics import mean
from statistics import pstdev
import winsound


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

datasets = [
'E:\\python-projects\\snptee\\dataset_audios\\original',
'E:\\python-projects\\snptee\\dataset_audios\\et30',
'E:\\python-projects\\snptee\\dataset_audios\\et35',
'E:\\python-projects\\snptee\\dataset_audios\\et40',
'E:\\python-projects\\snptee\\dataset_audios\\et45',
'E:\\python-projects\\snptee\\dataset_audios\\et50',
'E:\\python-projects\\snptee\\dataset_audios\\et55',
'E:\\python-projects\\snptee\\dataset_audios\\agress0',
'E:\\python-projects\\snptee\\dataset_audios\\agress1',
'E:\\python-projects\\snptee\\dataset_audios\\agress2',
'E:\\python-projects\\snptee\\dataset_audios\\agress3',
'E:\\python-projects\\snptee\\dataset_audios\\sw03_w01',
'E:\\python-projects\\snptee\\dataset_audios\\sw03_w02',
'E:\\python-projects\\snptee\\dataset_audios\\sw03_w03',
'E:\\python-projects\\snptee\\dataset_audios\\sw05_w01',
'E:\\python-projects\\snptee\\dataset_audios\\sw05_w02',
'E:\\python-projects\\snptee\\dataset_audios\\sw05_w03'
]
myTable = PrettyTable(['Set','Total Num de Áudios', 'Média Num de Áudios', 'Duração total', 'Média Duração', 'Num de áudios > 20seg'])

for inputdirectory in datasets:
    diretorios_audios = []
    caminhos_audios = []
    for caminho, subdirs, files in os.walk(str(inputdirectory)):
        caminhos_audios.append(caminho)
        for name in  sorted(files, key=natural_keys):
            if ".wav" in name:
                diretorios_audios.append(os.path.join(caminho, name))
    
    quantidades_audios=[]
    quantidade=0
    for caminho in caminhos_audios:
        for base, dirs, files in os.walk(caminho):
            for Files in files:
                quantidade += 1
            
            quantidades_audios.append(quantidade)
            quantidade=0

    duracao_total = 0
    duracoes=[]
    for nome in diretorios_audios:
        samplerate, data = read(nome)
        duration = len(data)/samplerate
        duracoes.append(duration)
        duracao_total=duracao_total+duration
    
    folder = inputdirectory.split("\\")[-1]
    print("\nDataset: "+str(folder))
    print("Quantidade de arquivos: %.0f" % len(diretorios_audios))    
    print("Duração total: %.2f segundos" % duracao_total)
    print("Média Duração: %.2f" % mean(duracoes))
    print("Desvio Padrão Duração: %.2f" % pstdev(duracoes))
    print("Média Quantidade de Áudios: %.2f" % mean(quantidades_audios))
    
    count=0
    for duracao in duracoes:
        if duracao>20:
            count+=1
            
    print("Quantidade de audios maior que 20 seg: %.0f" % count)
    
    myTable.add_row([folder,'{:.2f}'.format(len(diretorios_audios)),'{:.2f}'.format(mean(quantidades_audios)),'{:.2f}'.format(duracao_total),'{:.2f}'.format(mean(duracoes)),'{:.2f}'.format(count)])
        

duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
print(myTable)
