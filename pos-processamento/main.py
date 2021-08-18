import csv
import re
import os
import string
import unicodedata
from tqdm import tqdm
from trocas import substituicoes
import numpy as np

def corrigePalavras(lista):
    text_new = []
    for word in lista:
        try:
            if substituicoes[word]:
                text_new.append(substituicoes[word])
        except:
            text_new.append(word)
    return text_new

def removeAcento(lista):
    clean_text = []
    for word in lista:
        nfkd = unicodedata.normalize('NFKD', word)
        palavras_sem_acento = u''.join([c for c in nfkd if not unicodedata.combining(c)])
        q = re.sub('[^a-zA-Z0-9 \\\]', ' ', palavras_sem_acento)
        clean_text.append(q.lower().strip())
    return clean_text

def removePontuacao(lista):
    clean_text = []
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    words = lista.split()
    for word in words:
        new_token = regex.sub(u'', word)
        if not new_token == u'':
            clean_text.append(new_token)
    return clean_text

def processamentoTexto(text):
    # remove pontuação
    text_sem_pontuacao = removePontuacao(text)
    # remove acento
    text_sem_acento = removeAcento(text_sem_pontuacao)
    # subistitui palavras transcritas erradas
    text_corrigido = corrigePalavras(text_sem_acento)
    # junta tokens
    frase = ' '.join(text_corrigido)
    return frase


inputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\input'
arquivos_csv = []
for caminho, subdirs, files in os.walk(inputdirectory):
    for name in files:
        if ".csv" in name:
            arquivos_csv.append(name)

for arquivo_csv in arquivos_csv:
    new_file = csv.reader(open(inputdirectory+"/"+arquivo_csv, "r"),delimiter='_')
    
    list_docs=[]
    list_labels=[]
    doc_words=[]
    
    for row in tqdm(list(new_file)):
        limpo = processamentoTexto(row[4])
        doc_words.append([row[0], limpo])
        list_docs.append(limpo)
    
    np_transcricoes_tratadas = np.asarray(doc_words)
    np.savetxt("output/"+arquivo_csv, np_transcricoes_tratadas, delimiter="_", fmt='%s')