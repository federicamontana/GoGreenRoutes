import pandas as pd
import os
import json

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
from utilities import read_dic, sentiment_lists

input = 'liwc'
dict_json = 'dict/nrc_en.json'
dict_dic = 'dict/LIWC2007_English080730.dic'
emotions_nrc =['fear', 'anger','trust','surprise','positive',
    'negative','sadness','disgust','joy','anticipation']
emotions_liwc = ['affect','posemo','negemo','anx','anger','sad',
    'social','family','friend','health','leisure','death'] 

class NLP():

    #Read dictionary  
    def read_json_dic(dict_json,dict_dic,emotions_nrc,emotions_liwc,input):
        if input == 'liwc':
            emotions = emotions_liwc
            dictionary,label = read_dic(dict_dic)
            words = list(dictionary.keys())

            with open('dict/liwc_dic.json', 'w') as fp:
                json.dump(dictionary, fp, indent=1)
            dizionario_json = 'dict/liwc_dic.json'
        else:
            dizionario_json = dict_json
            emotions = emotions_nrc
        df = pd.read_json(dizionario_json, orient ='index')
        df = df.fillna(0).T.head()
        df2 = pd.DataFrame()
        for emotion in emotions:
            df2[emotion] = df.apply(lambda i: i.astype(str).str.contains(emotion).any(), axis=0).astype(int)
        return df2  
    #Dictionary as df
    df = read_json_dic(dict_json,dict_dic,emotions_nrc,emotions_liwc,'liwc')
    #Create sentiment list
    sentiment_list = sentiment_lists(df)

    
        