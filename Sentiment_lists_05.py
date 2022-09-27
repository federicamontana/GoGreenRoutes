import pandas as pd
import numpy as np 
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path 
from Utility_Fede_04 import label,new_df

#Creo le liste dei sentimenti usate nel vocabolario
os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

df2 = pd.read_json('dict/nrc_en.json', orient ='index')
df2 = df2.fillna(0).T.head()
df3 = pd.DataFrame()
for i in label: new_df(i,df2,df3)
sentiment_list = []
for i in df3: sentiment_list.append(df3.loc[df3[i]!=0][i].reset_index()['index'].tolist())

fear_list = sentiment_list[0]
anger_list = sentiment_list[1]
trust_list = sentiment_list[2]
surprise_list = sentiment_list[3]
positive_list = sentiment_list[4]
negative_list = sentiment_list[5]
sadness_list = sentiment_list[6]
disgust_list = sentiment_list[7]
joy_list = sentiment_list[8]
anticipation_list = sentiment_list[9]

