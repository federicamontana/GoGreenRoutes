import pandas as pd
import numpy as np 
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from pathlib import Path 
from matplotlib import cm
from PIL import Image

from Utility_Fede import aggregation_byparks,label,explode
from Sentiment_lists import fear_list, anger_list, trust_list, surprise_list, positive_list, negative_list, sadness_list, disgust_list, joy_list, anticipation_list

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

df = pd.read_csv('dataframe/df_completec.csv')

#STEP1: Vedo il sentimento in media nei parchi

#Return affect dictionary : in ogni tweet le parole con il sentimento associato
df["emotions_dict"] = df["text1"].apply(lambda x: NRCLex(x).affect_dict) 
#Return affect frequencies
df["emotions_freq"] = df["text1"].apply(lambda x: NRCLex(x).affect_frequencies)
#Return highest emotions
df["emotions_top"] = df["text1"].apply(lambda x: NRCLex(x).top_emotions)

#Lo faccio per 3 parchi diversi e li confronto
# ballyhoura_df,aggr,df_ball = aggregation_byparks('ballyhoura',df)
# westfields_df,aggr, df_west = aggregation_byparks('westfields',df)
# shannon_df,aggr, df_shannon = aggregation_byparks('shannon',df)
# ted_russel_df,aggr, df_ted = aggregation_byparks('ted russel',df)
# df_parks = pd.concat([ballyhoura_df, westfields_df, shannon_df, ted_russel_df], axis=1)

#emotional dataframe sorted with most common words
df_em_mc = pd.DataFrame({'emotion': label, 'aggregation': aggr}).sort_values(by=['aggregation'],ascending=False)

#STEP2: Quale parole danno questi sentimenti?
#In Sentiment_lists.py sono presente le liste dei sentimenti pos/neg ecc presi dal vocabolario NRCLex
#Vedo quante parole nel testo pulito text1 sono presenti nella lista e nel parco che scelgo

#!!!!!!!PARAMETRI DA PASSARE!!!
park_name = 'arthur'
emotion_counting_df,aggr,df_park = aggregation_byparks(park_name,df)

lista = positive_list
#in df_result sono presente le parole con i conteggi
#df_match_list è il dataframe con la la lista delle parole metchate nella lista sentiemnt
df_result,df_match_list = explode(df_park,lista)
df_result = df_result.reset_index(name="count") # con reset_index mi trasformo la serie in dataframe

word = "mayor"
#Extract tweet with certain words
#nella colonna result, per ogni riga metto insieme tutte le parole che erano nella lista e vedo se contengono la parola che mi interessa
explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"\b"+word+r"\b", regex=True)]






