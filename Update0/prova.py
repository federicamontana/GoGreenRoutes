import pandas as pd
import os 
import matplotlib.pyplot as plt
import seaborn as sns
import json 
from Read_dictionary_03 import emotions_liwc as emotions
os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes/Update0')
path_plot = os.path.abspath('plots')
#df0 = pd.read_csv('df_prova.csv', index_col=[0])
from Read_dictionary_03 import df1 as df3
from nltk import word_tokenize
from Utility_Fede_2 import new_df, read_dic
import contractions
park_list = ['ballyhoura','castletroy','shannon','arthur']

def text_emotion(df, column, df3):
    #df : contiene i tweet
    #df3 : vocabolario
    '''
    INPUT: DataFrame, string
    OUTPUT: the original DataFrame with ten new columns for each emotion
    '''

    new_df = df.copy()

    emotions = df3.columns.drop('word')
    emo_df = pd.DataFrame(0, index=df.index, columns=emotions)
    for i, row in new_df.iterrows():
        document = word_tokenize(new_df.loc[i][column])
        for word in document:
            emo_score = df3[df3.word == word]
            if not emo_score.empty:
                for emotion in emotions:
                    emo_df.at[i, emotion] += emo_score[emotion]

    new_df = pd.concat([new_df, emo_df], axis=1)

    return new_df

df1 = pd.read_csv('df_tweet.csv')
df = df1[['text','text1']].head(10)
df3 = pd.read_csv('dizionario.csv')


import spacy
nlp = spacy.load('en_core_web_sm')
sentence = "The striped bats are hanging on their feet for best"
doc = nlp(sentence)
#" ".join([token.lemma_ for token in doc])
document = [token.lemma_ for token in doc]
new_df = df.copy()
import re
emotions = df3.columns.drop('word')
emo_df = pd.DataFrame(0, index=df.index, columns=emotions)
for i,row in new_df.iterrows(): #i= indice, row = riga= tweet
    for w in df3.columns:
        frase = new_df.loc[i]['text1']
        parola = re.findall(r"\b"+w,frase)
    document = word_tokenize(frase)
    for word in document:
        emo_score = df3[df3.word == word]
        if not emo_score.empty:
            for emotion in emotions:
                emo_df.at[i, emotion] += emo_score[emotion]

new_df = pd.concat([new_df, emo_df], axis=1)

new_df = df.copy()
emotions = df3.columns.drop('word')
emo_df = pd.DataFrame(0, index=df.index, columns=emotions)
for word in df3.word:
    emo_score =


df = pd.DataFrame({"text1": ["Hi abandon", "I have been abandoned", "abilities", "i zz adore"]})
#lista = []
for tweet in df['text1']: 
    for w in df3.word:
        #lista.append(bool(re.findall(r"\b"+w,frase)))
        s = pd.Series((bool(re.findall(r"\b"+w,tweet))))



        
df0 = df3[df3[emotions].any(axis=1)]