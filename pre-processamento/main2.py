import collections
import contextlib
import sys
import wave
import webrtcvad
import os
import glob
from pydub import AudioSegment
from auditok import split

def main():
    inputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\input'
    outputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\output'
    
    directory = os.path.dirname(os.path.realpath(__file__)) + '\input\*.wav'
    
    # divide os audios em regioes e salva cada regiao de cada audio para uma pasta separada
    nomes_audios = []
    for nome in os.listdir(inputdirectory):
        if ".wav" in nome:
            nomes_audios.append(nome)
            
    for nome_audio in nomes_audios:
        cont=0
        audio_regioes = split(os.path.join(inputdirectory, nome_audio),
            min_dur=0.1,     # minimum duration of a valid audio event in seconds
            max_dur=20,      # maximum duration of an event
            max_silence=0.2,  # maximum duration of tolerated continuous silence within an event
            energy_threshold=50
        )
        os.makedirs(os.path.join(outputdirectory,nome_audio.replace('.wav', '')), exist_ok=True)
        for region in audio_regioes:
            region.save(os.path.join(outputdirectory,nome_audio.replace('.wav', ''))+'/'+nome_audio.replace('.wav', '_')+str(cont)+".wav")
            cont=cont+1

    # adiciona xs de silencio no inicio dos audios para melhor processamento do wit
    silencio_dur = input('Informe o silencio a ser adicionado (seg): ')
    if float(silencio_dur) != 0:
        # pegando caminho e nomes dos audios - saida
        diretorios_audios_saida = []
        for path, subdirs, files in os.walk(outputdirectory):
            for name in files:
                if ".wav" in name:
                    diretorios_audios_saida.append(os.path.join(path, name))
                
        silent_segment = AudioSegment.silent(duration=float(silencio_dur)*1000)
        cont=0
        for audio_saida in diretorios_audios_saida:
            audio = AudioSegment.from_wav(audio_saida)
            final_audio = silent_segment + audio + silent_segment
            final_audio.export(audio_saida, format="wav")


if __name__ == '__main__':
    main()




