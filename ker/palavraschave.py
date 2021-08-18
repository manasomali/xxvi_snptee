# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 19:17:43 2021

@author: mathe
"""
keywords={
    'maquin':1,
    'horario':2,
    'deslig':3,
    'reduz':4,
    'geracao':5,
    'mw':6,
    'sgi':7,
    'kv':8,
    'chuva':9,
    'disjuntor':10,
    'usina':11,
    'tensao':12,
    'conversor':13,
    'intervencao':14,
    'potencia':15,
    'barra':16,
    'milimetro':17,
    'elev':18,
    'nivel':19,
    'metro':20,
    'manobr':21,
    'reservatorio':22,
    'gerar':23,
    'compens':24,
    'vazao':25,
    'watt':26,
    'montante':27,
    'documento':28,
    'prorrog':29,
    'vertimento':30
}
count_keywords={
    'maquin':0,
    'horario':0,
    'deslig':0,
    'reduz':0,
    'geracao':0,
    'mw':0,
    'sgi':0,
    'kv':0,
    'chuva':0,
    'disjuntor':0,
    'usina':0,
    'tensao':0,
    'conversor':0,
    'intervencao':0,
    'potencia':0,
    'barra':0,
    'milimetro':0,
    'elev':0,
    'nivel':0,
    'metro':0,
    'manobr':0,
    'reservatorio':0,
    'gerar':0,
    'compens':0,
    'vazao':0,
    'watt':0,
    'montante':0,
    'documento':0,
    'prorrog':0,
    'vertimento':0
}
vec_keywords = [
    'maquin',
    'horario',
    'deslig',
    'reduz',
    'geracao',
    'mw',
    'sgi',
    'kv',
    'chuva',
    'disjuntor',
    'usina',
    'tensao',
    'conversor',
    'intervencao',
    'potencia',
    'barra',
    'milimetro',
    'elev',
    'nivel',
    'metro',
    'manobr',
    'reservatorio',
    'gerar',
    'compens',
    'vazao',
    'watt',
    'montante',
    'documento',
    'prorrog',
    'vertimento']
keywords_to_pretty={
    'maquin':'máquina',
    'horario':'horário',
    'deslig':'desligar',
    'reduz':'reduz',
    'geracao':'geração',
    'mw':'mw',
    'sgi':'sgi',
    'kv':'kv',
    'chuva':'chuva',
    'disjuntor':'disjuntor',
    'usina':'usina',
    'tensao':'tensão',
    'conversor':'conversor',
    'intervencao':'intervenção',
    'potencia':'potência',
    'barra':'barra',
    'milimetro':'milímetro',
    'elev':'elevar',
    'nivel':'nível',
    'metro':'metro',
    'manobr':'manobra',
    'reservatorio':'reservatório',
    'gerar':'gerar',
    'compens':'compensa',
    'vazao':'vazão',
    'watt':'watt',
    'montante':'montante',
    'documento':'documento',
    'prorrog':'prorrogar',
    'vertimento':'vertimento'
}