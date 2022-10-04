import pandas as pd
import os

#Creo le liste dei sentimenti usate nel vocabolario
os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

from Read_dictionary_03 import df2_liwc,df2_nrc

sentiment_list = []
for i in df2_nrc: 
    sentiment_list.append(df2_nrc.loc[df2_nrc[i]!=0][i].reset_index()['index'].tolist())

#NRC lists
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
