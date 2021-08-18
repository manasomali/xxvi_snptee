# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 19:12:09 2021

@author: mathe
"""
from palavraschave import keywords
from palavraschave import keywords_to_pretty
from palavraschave import vec_keywords
from palavraschave import count_keywords


class KER:
    def __init__(self, truth="", hypothesis="", verbosity=False):
        self.truth = truth
        self.hypothesis = hypothesis
        self.vec_truth = truth.split()
        self.vec_hypothesis = hypothesis.split()
        self.verbosity = verbosity
    
    def claculate(self):
        t_kw_apperance = self.create_vec(self.vec_truth)
        h_kw_apperance = self.create_vec(self.vec_hypothesis)
        num_flase_kw = self.false_kw(t_kw_apperance, h_kw_apperance)
        num_true_kw = self.true_kw(t_kw_apperance, h_kw_apperance)
        num_kw = self.count_kw(t_kw_apperance)
        if self.verbosity==True:
            print(t_kw_apperance)
            print(h_kw_apperance)
            print(num_flase_kw)
            print(num_true_kw)
            print(num_kw)
            
        if num_kw==0:
            return 0
        return (num_flase_kw+num_true_kw)/num_kw
    
    def create_vec(self, doc):
        np_vec = []
        for word in doc:
            for kw in vec_keywords:
                if word.startswith(kw):
                    np_vec.append(keywords[kw])
                    
        return np_vec
                
    def false_kw(self, vec_t, vec_h):
        f=0
        for h in vec_h:
            if not h in vec_t:
                f+=1
                
        return f
    
    def true_kw(self, vec_t, vec_h):
        m=0
        for t in vec_t:
            if not t in vec_h:
                m+=1

        return m
    
    def count_kw(self, vec_t):
        return len(vec_t)
    
    def generate_texto_wc(self, corpus):
        
        kws=self.cont_apperance_kws(corpus)
        total_aparicoes=0
        for kw in kws:
            total_aparicoes+=kws[kw]
        
        print(total_aparicoes)
        cont=0
        for kw in kws:
            while kws[kw]>cont:
                print(keywords_to_pretty[kw], end = ' ')
                cont+=1
            cont=0
    
    def cont_apperance_kws(self, corpus):
        for word in corpus.split():
            for kw in vec_keywords:
                if word.startswith(kw):
                    count_keywords[kw]+=1
        print(count_keywords)
        return count_keywords
    
#t="por favor reduz tres mw na maquin um e elev dois kv de tensao"
#h="por favor reduz tres metro na maquin um e elev dois de tensao"
#KER=KER(t,h)
#print('ker: '+str(KER.claculate()))