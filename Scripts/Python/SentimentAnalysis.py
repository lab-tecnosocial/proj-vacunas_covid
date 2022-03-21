# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 17:10:11 2022

@author: MarioPC
"""

import pandas as pd
from pysentimiento import create_analyzer



df = pd.read_csv("vaccine_comments.csv")

sentiment = list()
emotions = list()
hate_level = list()

analyzer = create_analyzer(task="sentiment", lang="es")  
emotion_analyzer = create_analyzer(task="emotion", lang="es")
hate_speech_analyzer = create_analyzer(task="hate_speech", lang="es")

for comment in df['comments']:
               
    rets_sent = analyzer.predict(comment) 
    sentiment.append(rets_sent.probas)
       
    rets_emo = emotion_analyzer.predict(comment) 
    emotions.append(rets_emo.probas)
    
    rets_hate = hate_speech_analyzer.predict(comment) 
    hate_level.append(rets_hate.probas)


df_s = pd.DataFrame(sentiment)        
df_e = pd.DataFrame(emotions)        
df_h = pd.DataFrame(hate_level)        

df_analysis =  pd.concat([df, df_s, df_e, df_h], axis=1)
df_analysis.to_csv('vaccine_comments_sentiment_analysis.csv',index=False,encoding='utf-8')