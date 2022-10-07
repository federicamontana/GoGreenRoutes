import pandas as pd
import os 
from nltk import word_tokenize
import re

def text_emotion(df_tweet, column, df_dic):
    '''
    INPUT: DataFrame, string
    OUTPUT: the original DataFrame with ten new columns for each emotion
    '''
    df = df_tweet.copy()
    #Set index as column and call it 'word'
    #df_dic = df_dic.reset_index().rename(columns = {'index':'word'})
    emotions = df_dic.columns.drop('word')
    emo_df = pd.DataFrame(0, index=df.index, columns=emotions)
    for i,row in df.iterrows(): 
        l=[]
        tweet = word_tokenize(df.loc[i]['text1'])
        for wt in tweet:
            for word in df_dic['word']:
                l.append(bool(re.findall(r"\b"+word,wt)))
            s = pd.Series(l,name = 'word')
            emo_score = df_dic[s]
            l=[]
            if not emo_score.empty:
                for emotion in emotions:
                    emo_df.at[i, emotion] += emo_score[emotion]
    df = pd.concat([df, emo_df], axis=1)
    #Remove i tweet che non hanno associato nessun sentimento
    df = df[df[emotions].any(axis=1)]
    return df



