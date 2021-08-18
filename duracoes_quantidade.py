# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 19:40:43 2021

@author: mathe
"""

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

root = Tk()
root.withdraw() 
inputdirectory = filedialog.askdirectory()
diretorios_audios = []
for caminho, subdirs, files in os.walk(str(inputdirectory)):
    for name in  sorted(files, key=natural_keys):
        if ".wav" in name:
            diretorios_audios.append(os.path.join(caminho, name))

duracao_total = 0
duracoes=[]
for nome in tqdm(diretorios_audios):
    samplerate, data = read(nome)
    duration = len(data)/samplerate
    duracoes.append(duration)
    duracao_total=duracao_total+duration

folder = inputdirectory.split("\\")
print("\n"+str(folder[-1])+"\n")
print("Quantidade de arquivos: %.0f" % len(diretorios_audios))    
print("Duração total: %.2f segundos" % duracao_total)
print("Média: %.2f" % mean(duracoes))
print("Desvio Padrão: %.2f" % pstdev(duracoes))

count=0
for duracao in duracoes:
    if duracao>=20:
        count+=1
        
print("Quantidade de audios maior que 20 seg: %.0f" % count)

duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)