import pandas as pd
import numpy as np 
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
#https://github.com/metalcorebear/NRCLex/blob/cda50c7d7c51709acf506b815037cb376572a629/README.md

df = pd.read_csv('dataframe/dfc.csv') #dfc.csv is the cleaned dataframe

filepath = "dict/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t')

### STEP1 - vedere il sentimento in media nel parco

# Return affect dictionary : in ogni tweet le parole con il sentimento associato
df["emotions_dict"] = df["text1"].apply(lambda x: NRCLex(x).affect_dict) 
#Return affect frequencies
df["emotions_freq"] = df["text1"].apply(lambda x: NRCLex(x).affect_frequencies)
#Return highest emotions
df["emotions_top"] = df["text1"].apply(lambda x: NRCLex(x).top_emotions)

# Select dataframe with cleaned text (text1), emotions_dict, emotions_freq, emotions_top
df2 = df[["text1","emotions_dict","emotions_freq","emotions_top"]]
df_f= df2[["text1","emotions_freq"]]

#Concateno il dataframe df_f in cui ho preso solo la colonna text1 con drop
# e quello in cui ho estratto il dizionario in formato pandas e messo le emozioni in colonna
#con .drop elimino la colonna anticip che è in più dato che esiste anticipation
df_s = pd.concat([df_f.drop(['emotions_freq'], axis = 1), df_f['emotions_freq'].apply(pd.Series).drop("anticip", axis=1)], axis = 1)

#Replace NaN with 0
df_s = df_s.replace(np.nan,0)

#recall the function to compute the mean
# i indicate all the emotions 
from notebook import Utility_Fede 
from Utility_Fede import aggregation
aggr = []
labels = []
for i in df_f['emotions_freq'].apply(pd.Series).drop("anticip", axis=1) : aggregation(i,df_s,aggr,labels)

#Plot
#create pie chart
plt.pie(aggr, labels = labels) #, autopct='%.0f%%'
sns.set(rc={'figure.figsize':(20,10)})
plt.show()

 
