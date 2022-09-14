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
df = pd.read_csv('dataframe/df_completec.csv')

#STEP1: Vedo il sentimento in media nei parchi

#Return affect dictionary : in ogni tweet le parole con il sentimento associato
df["emotions_dict"] = df["text1"].apply(lambda x: NRCLex(x).affect_dict) 
#Return affect frequencies
df["emotions_freq"] = df["text1"].apply(lambda x: NRCLex(x).affect_frequencies)
#Return highest emotions
df["emotions_top"] = df["text1"].apply(lambda x: NRCLex(x).top_emotions)

#Compute the sentiment in the park with aggregation_byparks
ballyhoura_df,aggr = aggregation_byparks('ballyhoura',df)
#create pie chart

#emotional dataframe sorted with most common words
df_em_mc = pd.DataFrame({'emotion': label, 'aggregation': aggr}).sort_values(by=['aggregation'],ascending=False)

#Lo faccio per 3 parchi diversi e li confronto
ballyhoura_df,aggr = aggregation_byparks('ballyhoura',df)
westfields_df,aggr = aggregation_byparks('westfields',df)
shannon_df,aggr = aggregation_byparks('shannon',df)
ted_russel_df,aggr = aggregation_byparks('ted russel',df)
df_parks = pd.concat([ballyhoura_df, westfields_df, shannon_df, ted_russel_df], axis=1)

#STEP2: Quale parole danno questi sentimenti?
#In Sentiment_lists.py sono presente le liste dei sentimenti pos/neg ecc presi dal vocabolario NRCLex

#Vedo quante parole nel testo pulito text1 sono presenti nella lista positive
lista = negative_list
df_result = explode(df,lista).reset_index(name="count") # con reset_index mi trasformo la serie in dataframe






