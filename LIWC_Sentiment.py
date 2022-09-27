import pandas as pd
import os
import liwc
import json

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

from Utility_Fede_04 import new_df, _parse_categories, _parse_lexicon, read_dic, text_emotion

#https://github.com/chbrown/liwc-python/blob/master/liwc/dic.py
# Lettura dizionario liwc
dizionario,label = read_dic('dict/LIWC2007_English080730.dic')
words = list(dizionario.keys())

with open('liwc_dic.json', 'w') as fp:
    json.dump(dizionario, fp, indent=1)

#from dictionary (with different length) to df
df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dizionario.items()])).fillna(0)

#Create a new dataframe df2
df2 = pd.DataFrame(
                  index=pd.Index(words),
                  columns=pd.Index(label)).fillna(0)

#Create a df which return df2 that have sentiment in the columns and words as rows
for i in label: new_df(i,df,df2)
#Rest the index, which contains the words as column called word
df2.reset_index(inplace=True)
df2 = df2.rename(columns = {'index':'word'})

#Select the emotion we want to study
df3 = df2[['word','affect','posemo','negemo','anx','anger','sad','social','family','friend','health','leisure','death']]

#Read the tweet dataframe taken from Mongodb and cleaned
tweet_data = pd.read_csv('dataframe/df_completec.csv')
#Select just two columns
tweet_data = tweet_data[['_id','text1']]

#Apply text_emotion function which return df with 1 when the word corresponds the emotion and 0 if not
df_final = text_emotion(tweet_data, 'text1', df3)
df_final.head()