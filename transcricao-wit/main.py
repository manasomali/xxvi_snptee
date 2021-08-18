from dotenv import load_dotenv
import os
import speech_recognition as sr
import time
import re
import numpy as np
from multiprocessing import Pool, freeze_support
from tkinter import Tk
from tkinter import filedialog
import tqdm
from natsort import natsorted
import winsound


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

# codigo do wit
def transcricaoWit(diretorio_audio):
    # setup variaveis do ambiente
    load_dotenv('.env')
    WIT_AI_KEY=os.getenv('WIT_AI_KEY')
    
    transcricao=""
    r = sr.Recognizer()
    with sr.AudioFile(diretorio_audio) as source:
        audio = r.record(source)
        try:
            transcricao = r.recognize_wit(audio, key=WIT_AI_KEY)
        except sr.UnknownValueError:
            transcricao = "misunderstanding"
        except sr.RequestError:
            transcricao = "error in requisition"
        
        while transcricao=="error in requisition":
            # espera 60 segundos pois a api é limitada em 60 requisiçoes por minuto
            time.sleep(61)
            try:
                transcricao = r.recognize_wit(audio, key=WIT_AI_KEY)
            except sr.UnknownValueError:
                transcricao = "misunderstanding"
            except sr.RequestError:
                transcricao = "error in requisition"
        
        # escreve resultado das transcrições no arquivo output/transcricoes_wit.txt
        with open("output/transcricoes_wit.txt", "a") as txt_file:
            txt_file.write(str(diretorio_audio.split("\\").pop().replace(".wav", "")) + "_" + str(transcricao) + "\n")
            
        return [str(diretorio_audio.split("\\").pop().replace(".wav", "")), str(transcricao)]

if __name__ == '__main__':
    freeze_support()
    with open("output/transcricoes_wit.txt", "w") as txt_file:
        txt_file.write(str(""))
        
    inicio = time.time()
    
    root = Tk()
    root.withdraw() 
    inputdirectory = filedialog.askdirectory()
    diretorios_audios = []
    for caminho, subdirs, files in os.walk(str(inputdirectory)):
        for name in  sorted(files, key=natural_keys):
            if ".wav" in name:
                diretorios_audios.append(os.path.join(caminho, name))
    
    with Pool() as pool:
        transcricoes = list(pool.map(transcricaoWit, diretorios_audios))
           
    fim = time.time()
    print("\n"+str(inputdirectory)+"\n")
    print("Tempo de processamento (seg):", fim - inicio)

    # cria um csv com as transcricoes em ordem
    transcricoes = natsorted(transcricoes)
    np_transcricoes = np.asarray(transcricoes)
    np.savetxt("output/transcricoes_wit.csv", np_transcricoes, delimiter="_", fmt='%s')
    transcricoes_agrupadas=[]
    transcricao_agrupada = ""
    nome_temp=transcricoes[0][0].rsplit("_", 1).pop(0)
    cont=1
    for transcricao in np_transcricoes:
        nome=transcricao[0].rsplit("_", 1).pop(0)
        if(nome!=nome_temp):
            transcricoes_agrupadas.append([nome_temp,transcricao_agrupada.strip()])
            transcricao_agrupada = transcricao[1]
        else:
            transcricao_agrupada=transcricao_agrupada+" "+transcricao[1]
        if(cont== len(np_transcricoes)):
            transcricoes_agrupadas.append([nome_temp,transcricao_agrupada])
            
        cont+=1    
        nome_temp=nome
    
    np_transcricoes_agrupadas = np.asarray(transcricoes_agrupadas)
    np.savetxt("output/transcricoes_wit_agrupados.csv", np_transcricoes_agrupadas, delimiter="_", fmt='%s')
    
    duration = 2500
    freq = 440
    winsound.Beep(freq, duration)