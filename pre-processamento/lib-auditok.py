import os
from auditok import split

def main():
    inputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\input'
    outputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\output'

#auditok
#md = 0.2 et = 30 ok
#md = 0.2 et = 35 ok
#md = 0.2 et = 40 ok
#md = 0.2 et = 45 ok
#md = 0.2 et = 50 ok
#md = 0.2 et = 55 ok
#
            
    # divide os audios em regioes e salva cada regiao de cada audio para uma pasta separada
    nomes_audios = []
    for nome in os.listdir(inputdirectory):
        if ".wav" in nome:
            nomes_audios.append(nome)
            
    for nome_audio in nomes_audios:
        cont=0
        audio_regioes = split(os.path.join(inputdirectory, nome_audio),
            min_dur=0.2,     # minimum duration of a valid audio event in seconds
            max_dur=20,      # maximum duration of an event
            max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
            energy_threshold=35 # threshold of detection
        )
        os.makedirs(os.path.join(outputdirectory,nome_audio.replace('.wav', '')), exist_ok=True)
        for region in audio_regioes:
            region.save(os.path.join(outputdirectory,nome_audio.replace('.wav', ''))+'/'+nome_audio.replace('.wav', '_')+str(cont)+".wav")
            cont=cont+1
    
if __name__ == '__main__':
    main()




