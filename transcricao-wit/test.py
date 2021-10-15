# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 15:40:44 2021

@author: mathe
"""
datasets = ['E:\python-projects\snptee\dataset_audios\semsilencio0_separado0',
            'E:\python-projects\snptee\dataset_audios\semsilencio0_separado0ponto1',
            'E:\python-projects\snptee\dataset_audios\semsilencio0_separado0ponto1_somenteinicio',
            'E:\python-projects\snptee\dataset_audios\semsilencio0_separado0ponto2',
            'E:\python-projects\snptee\dataset_audios\semsilencio0_separado0ponto2_somenteinicio',
            'E:\python-projects\snptee\dataset_audios\semsilencio3_separado0',
            'E:\python-projects\snptee\dataset_audios\semsilencio3_separado0ponto1',
            'E:\python-projects\snptee\dataset_audios\semsilencio3_separado0ponto2',
            'E:\python-projects\snptee\dataset_audios\separado0',
            'E:\python-projects\snptee\dataset_audios\separado0ponto1',
            'E:\python-projects\snptee\dataset_audios\separado0ponto2',
            'E:\python-projects\snptee\dataset_audios\separado0ponto3',
            'E:\python-projects\snptee\dataset_audios\separado0ponto4',
            'E:\python-projects\snptee\dataset_audios\separado0ponto5']
for dataset in datasets:    
    print(dataset.split('\\')[-1])