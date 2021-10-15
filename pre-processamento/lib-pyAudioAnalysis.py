# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 16:03:04 2021

@author: mathe
"""
import os
import glob
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import scipy.io.wavfile as wavfile
import winsound

#
#sw = 0.1 w = 0.1 ok
#sw = 0.1 w = 0.2 ok
#sw = 0.1 w = 0.3 ok
#sw = 0.3 w = 0.1 ok
#sw = 0.3 w = 0.2 ok
#sw = 0.3 w = 0.3 ok
#sw = 0.5 w = 0.1 ok
#sw = 0.5 w = 0.2 ok
#sw = 0.5 w = 0.3 ok


outputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\output'

directory = os.path.dirname(os.path.realpath(__file__)) + '\input\*.wav'
caminhos = (glob.glob(directory))
for caminho in caminhos:
        [Fs, x] = aIO.read_audio_file(caminho)
        segmentLimits = aS.silence_removal(x, 
                                      Fs, 
                                      0.05, 
                                      0.05, 
                                      smooth_window = 0.5, 
                                      weight = 0.3, 
                                      plot = False)
        
        nome_audio=caminho.split("\\")[-1]
        cont=0
        os.makedirs(os.path.join(outputdirectory,nome_audio.replace('.wav', '')), exist_ok=True)
        for i, s in enumerate(segmentLimits):
            strOut = os.path.join(outputdirectory,nome_audio.replace('.wav', ''))+'/'+nome_audio.replace('.wav', '_')+str(cont)+".wav"
            wavfile.write(strOut, Fs, x[int(Fs * s[0]):int(Fs * s[1])])
            cont+=1
            
duration = 1500
freq = 440
winsound.Beep(freq, duration)