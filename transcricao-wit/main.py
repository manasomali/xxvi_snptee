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
from wit import Wit
from scipy.io.wavfile import read

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def transcricaoWitSr(diretorio_audio):
    # setup variaveis do ambiente
    load_dotenv('.env')
    WIT_AI_KEY=os.getenv('WIT_AI_KEY')
    
    samplerate, data = read(diretorio_audio)
    duration = len(data)/samplerate
    if duration>20:
        return [str(diretorio_audio.split("\\").pop().replace(".wav", "")), ""]    
    
    transcricao=""
    r = sr.Recognizer()
    with sr.AudioFile(diretorio_audio) as source:
        audio = r.record(source)
        try:
            transcricao = r.recognize_wit(audio, key=WIT_AI_KEY)
        except sr.UnknownValueError:
            transcricao = ""
        except sr.RequestError:
            transcricao = "error in requisition"
        
        while transcricao=="error in requisition":
            # espera 60 segundos pois a api é limitada em 60 requisiçoes por minuto
            time.sleep(61)
            try:
                transcricao = r.recognize_wit(audio, key=WIT_AI_KEY)
            except sr.UnknownValueError:
                transcricao = ""
            except sr.RequestError:
                transcricao = "error in requisition"
        
        # escreve resultado das transcrições no arquivo output/transcricoes_wit.txt
        with open("output/transcricoes_wit_sr.txt", "a") as txt_file:
            txt_file.write(str(diretorio_audio.split("\\").pop().replace(".wav", "")) + "_" + str(transcricao) + "\n")
            
        return [str(diretorio_audio.split("\\").pop().replace(".wav", "")), str(transcricao)]

def transcricaoWitNativa(diretorio_audio):
    load_dotenv('.env')
    WIT_AI_KEY=os.getenv('WIT_AI_KEY')
    client = Wit(access_token=WIT_AI_KEY)
    transcricao = ""
    
    samplerate, data = read(diretorio_audio)
    duration = len(data)/samplerate
    if duration>20:
        return [str(diretorio_audio.split("\\").pop().replace(".wav", "")), ""]
    
    try:
        with open(diretorio_audio, 'rb') as f:
            transcricao = client.speech(f, {'Content-Type': 'audio/wav'})
    except:
        transcricao = "error in requisition"
            
    while transcricao=="error in requisition":
        time.sleep(61)
        try:
            with open(diretorio_audio, 'rb') as f:
                transcricao = client.speech(f, {'Content-Type': 'audio/wav'})
        except:
            transcricao = "error in requisition"
        
    with open("output/transcricoes_wit_nativo.txt", "a") as txt_file:
        txt_file.write(str(diretorio_audio.split("\\").pop().replace(".wav", "")) + "_" + str(transcricao['text']) + "\n")
        
    return [str(diretorio_audio.split("\\").pop().replace(".wav", "")), str(transcricao['text'])]


if __name__ == '__main__':
    
    datasets = [
               'E:\\python-projects\\snptee\\dataset_audios\\agress0',
               'E:\\python-projects\\snptee\\dataset_audios\\agress1',
               'E:\\python-projects\\snptee\\dataset_audios\\agress2',
               'E:\\python-projects\\snptee\\dataset_audios\\agress3',
               'E:\\python-projects\\snptee\\dataset_audios\\et30',
               'E:\\python-projects\\snptee\\dataset_audios\\et35',
               'E:\\python-projects\\snptee\\dataset_audios\\et40',
               'E:\\python-projects\\snptee\\dataset_audios\\et45',
               'E:\\python-projects\\snptee\\dataset_audios\\et50',
               'E:\\python-projects\\snptee\\dataset_audios\\et55',
               'E:\\python-projects\\snptee\\dataset_audios\\sw03_w01',
               'E:\\python-projects\\snptee\\dataset_audios\\sw03_w02',
               'E:\\python-projects\\snptee\\dataset_audios\\sw03_w03',
               'E:\\python-projects\\snptee\\dataset_audios\\sw05_w01',
               'E:\\python-projects\\snptee\\dataset_audios\\sw05_w02',
               'E:\\python-projects\\snptee\\dataset_audios\\sw05_w03'
            ]
    
    opcao=input("1 - Speech Recognition \n2 - Nativo \n3 - Ambos\n-->")
    tempos=[]
    freeze_support()
    for dataset in datasets:
        
        with open('output/transcricoes_wit_nativo.txt', "w") as txt_file:
            txt_file.write(str(""))
            
        with open('output/transcricoes_wit_nativo.txt', "w") as txt_file:
            txt_file.write(str(""))
            
        inicio = time.time()
        
        
        diretorios_audios = []
        transcricoes_sr=[]
        transcricoes_nativo=[]
        for caminho, subdirs, files in os.walk(str(dataset)):
            for name in  sorted(files, key=natural_keys):
                if ".wav" in name:
                    diretorios_audios.append(os.path.join(caminho, name))
        
        if opcao=='1' or opcao=='3':
            with Pool() as pool:
                transcricoes_sr = list(pool.map(transcricaoWitSr, diretorios_audios))
            
        if opcao=='2' or opcao=='3':
            with Pool() as pool:
                transcricoes_nativo = list(pool.map(transcricaoWitNativa, diretorios_audios))       
        
        fim = time.time()
        tempos.append([str(dataset.split('\\')[-1]),fim - inicio])
        print("\n"+str(dataset.split('\\')[-1])+"\n")
        print("Tempo de processamento (seg):", fim - inicio)
    
        # cria um csv com as transcricoes em ordem
        if transcricoes_sr!=[]:
            transcricoes_sr = natsorted(transcricoes_sr)
            np_transcricoes_sr = np.asarray(transcricoes_sr)
            #np.savetxt("output/transcricoes_wit_sr_separadas.csv", np_transcricoes_sr, delimiter="_", fmt='%s')
            transcricoes_sr_agrupadas=[]
            transcricao_sr_agrupada = ""
            nome_temp=transcricoes_sr[0][0].rsplit("_", 1).pop(0)
            cont=1
            for transcricao in np_transcricoes_sr:
                nome=transcricao[0].rsplit("_", 1).pop(0)
                if(nome!=nome_temp):
                    transcricoes_sr_agrupadas.append([nome_temp,transcricao_sr_agrupada.strip()])
                    transcricao_sr_agrupada = transcricao[1]
                else:
                    transcricao_sr_agrupada=transcricao_sr_agrupada+" "+transcricao[1]
                if(cont== len(np_transcricoes_sr)):
                    transcricoes_sr_agrupadas.append([nome_temp,transcricao_sr_agrupada])
                    
                cont+=1    
                nome_temp=nome
            
            np.savetxt('output\\' +dataset.split('\\')[-1]+ "_sr.csv", np.asarray(transcricoes_sr_agrupadas), delimiter="_", fmt='%s')
            
        # cria um csv com as transcricoes em ordem
        if transcricoes_nativo!=[]:
            transcricoes_nativo = natsorted(transcricoes_nativo)
            np_transcricoes_nativo = np.asarray(transcricoes_nativo)
            #np.savetxt("output/transcricoes_wit_nativo_separadas.csv", np_transcricoes_nativo, delimiter="_", fmt='%s')
            transcricoes_nativo_agrupadas=[]
            transcricao_nativo_agrupada = ""
            nome_temp=transcricoes_nativo[0][0].rsplit("_", 1).pop(0)
            cont=1
            for transcricao in np_transcricoes_nativo:
                nome=transcricao[0].rsplit("_", 1).pop(0)
                if(nome!=nome_temp):
                    transcricoes_nativo_agrupadas.append([nome_temp,transcricao_nativo_agrupada.strip()])
                    transcricao_nativo_agrupada = transcricao[1]
                else:
                    transcricao_nativo_agrupada=transcricao_nativo_agrupada+" "+transcricao[1]
                if(cont== len(np_transcricoes_nativo)):
                    transcricoes_nativo_agrupadas.append([nome_temp,transcricao_nativo_agrupada])
                    
                cont+=1    
                nome_temp=nome
            
            np.savetxt('output\\' +dataset.split('\\')[-1]+ "_nativo.csv", np.asarray(transcricoes_nativo_agrupadas), delimiter="_", fmt='%s')
            
        
        duration = 2500
        freq = 440
        winsound.Beep(freq, duration)