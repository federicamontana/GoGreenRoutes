import pandas as pd
import os
import json

#os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

from Utility_Fede_2 import new_df, read_dic

#LIWC
#Read a .dic file
dizionario,label = read_dic('dict/LIWC2007_English080730.dic')
words = list(dizionario.keys())

with open('dict\\liwc_dic.json', 'w') as fp:
    json.dump(dizionario, fp, indent=1)

#from dictionary (with different length) to pandas df
df_liwc = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dizionario.items()])).fillna(0)

#Create a new dataframe df2
df2_liwc = pd.DataFrame(
                  index=pd.Index(words),
                  columns=pd.Index(label)).fillna(0)

#Create a df which return df2 that have sentiment in the columns and words as rows
for i in label: new_df(i,df_liwc,df2_liwc)
emotions_liwc = ['affect','posemo','negemo','anx','anger','sad',
    'social','family','friend','health','leisure','death']
df2_liwc = df2_liwc[['affect','posemo','negemo','anx','anger','sad',
    'social','family','friend','health','leisure','death']]
#Rest the index, which contains the words as column called word
# df2_liwc.reset_index(inplace=True)
# df2_liwc = df2_liwc.rename(columns = {'index':'word'})

#Create list of sentiment
sentiment_list_liwc = []
for i in df2_liwc: 
    sentiment_list_liwc.append(df2_liwc.loc[df2_liwc[i]!=0][i].reset_index()['index'].tolist())

##############################################################################################
#NRC
df_nrc = pd.read_json('dict/nrc_en.json', orient ='index')
df_nrc = df_nrc.fillna(0).T.head()
df2_nrc = pd.DataFrame()
emotions_nrc =['fear',
    'anger',
    'trust',
    'surprise',
    'positive',
    'negative',
    'sadness',
    'disgust',
    'joy',
    'anticipation']
#Create a df which return df2 that have sentiment in the columns and words as rows
for i in emotions_nrc: new_df(i,df_nrc,df2_nrc)
# df2_nrc.reset_index(inplace=True)
# df2_nrc = df2_nrc.rename(columns = {'index':'word'})
#Create list of sentiment
sentiment_list_nrc = []
for i in df2_nrc: 
    sentiment_list_nrc.append(df2_nrc.loc[df2_nrc[i]!=0][i].reset_index()['index'].tolist())