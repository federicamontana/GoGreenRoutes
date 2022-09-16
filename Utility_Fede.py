import pandas as pd
from nrclex import NRCLex 
import numpy as np

label =['fear',
    'anger',
    'trust',
    'surprise',
    'positive',
    'negative',
    'sadness',
    'disgust',
    'joy',
    'anticipation']

#Compute the sentiment in the park
def aggregation_byparks(park,df):
    df = df[df['text1'].str.contains(park)] #cerco i tweet che hanno quel parco all'interno del testo
    df_f = pd.DataFrame(df['text1'])
    df_f["emotions_freq"] = df_f["text1"].apply(lambda x: NRCLex(x).affect_frequencies) #Return affect frequencies
    #Concateno il dataframe df_f in cui ho preso solo la colonna text1 con drop
    # e quello in cui ho estratto il dizionario in formato pandas e messo le emozioni in colonna
    #con .drop elimino la colonna anticip che è in più dato che esiste anticipation
    df_s = pd.concat([df_f.drop(['emotions_freq'], axis = 1), df_f['emotions_freq'].apply(pd.Series).drop("anticip", axis=1)], axis = 1)
    df_s = df_s.replace(np.nan,0) #Replace NaN with 0
    aggr = [] #lista che contiene le medie
    for i in df_f['emotions_freq'].apply(pd.Series).drop("anticip", axis=1) : aggregation(i,df_s,aggr)
    df_park= pd.DataFrame({park: aggr}, index = label)
    return df_park, aggr, df_f

    
#Compute the mean of the sentiment in a certain park 
def aggregation(sent,df_s,aggr):
    num = '{0:.3f}'.format(df_s[sent].mean()) #mean
    #print(sent, ": ",  num ) 
    num = float(num)
    return aggr.append(num)

def find_values(x,sent_list):
    results = []
    for value in sent_list:
        for word in x.split():
            if word == value:
                results.append(word)
    # return ' '.join(results)
    return results

def explode(df,sent_list):
    #inserisco nella colonna result le parole dei tweet che si trovano nella lista
    df['result'] = df['text1'].apply(lambda x: find_values(x,sent_list))
    #elimino le righe in cui la colonna è vuota (perchè non ha trovato niente)
    df_match_list = df[df['result'].map(lambda d: len(d)) > 0]
    df_result = df_match_list.explode("result").groupby(by="result")["result"].count().sort_values(ascending=False)
    return df_result, df_match_list 
    
def new_df(sent,df,df2):
    df2[sent] = df.apply(lambda i: i.astype(str).str.contains(sent).any(), axis=0).astype(int)
    return df2



# def count_words(sentlist,df_counter):
#     df_sentcount = df_counter[df_counter['words'].isin(sentlist)]
#     return df_sentcount.sort_values(by=['count'],ascending=False) 


# def find_words(sent,df,result_dn):
#     dn= pd.Series(df.apply(lambda i: i.astype(str).str.contains(sent).any(), axis=0),name='bool').to_frame().reset_index()
#     result_dn[sent] = dn.loc[dn['bool']==True].drop('bool', axis=1)
#     # mask = pd.Series(df.apply(lambda i: i.astype(str).str.contains(sent).any(), axis=0), name='bool')
#     # df2 = pd.DataFrame({sent:mask.index, 'bool':mask.values})
#     # result_dn[sent]= df2.loc[df2['bool']==True].drop('bool', axis=1)
#     return result_dn.to_dict(orient='list')
#https://stackoverflow.com/questions/64675132/pandas-find-all-words-from-row-in-dataframe-match-with-list