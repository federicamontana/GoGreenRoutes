import pandas as pd
import os
import json

from pymongo import MongoClient
from utilities import read_dic, sentiment_lists, extract_tweet

class Sentimen_Analysis():
    def __init__(self, input):
        #path
        self.path_data = os.path.abspath('dict')
        self.path_tweet = os.path.abspath('dataframe')
        self.path_plot = os.path.abspath('plots')
        #input vocabulary
        self.input = input
        self.dict_json = 'dict/nrc_en.json'
        self.dict_dic = 'dict/LIWC2007_English080730.dic'
        #emotions
        self.emotions_nrc =['fear', 'anger','trust','surprise','positive',
            'negative','sadness','disgust','joy','anticipation']
        self.emotions_liwc = ['affect','posemo','negemo','anx','anger','sad',
            'social','family','friend','health','leisure','death'] 
        #Connection with MONGODB
        # self.client = MongoClient('localhost', 27018)
        # self.db = self.client['ggr']
        # self.posts = self.db['limerick.posts']

    #Read dictionary  
    def read_json_dic(self) -> pd.DataFrame:
        if self.input == 'liwc':
            emotions = self.emotions_liwc
            dictionary,label = read_dic(self.dict_dic)
            words = list(dictionary.keys())

            with open('dict/liwc_dic.json', 'w') as fp:
                json.dump(dictionary, fp, indent=1)
            dizionario_json = 'dict/liwc_dic.json'
        else:
            dizionario_json = self.dict_json
            emotions = self.emotions_nrc
        df = pd.read_json(dizionario_json, orient ='index')
        df = df.fillna(0).T.head()
        df2 = pd.DataFrame()
        for emotion in emotions:
            df2[emotion] = df.apply(lambda i: i.astype(str).str.contains(emotion).any(), axis=0).astype(int)
        return df2

    # #Save tweet data in dataframe
    # def save_df_tweet(self):
    #     df_tweet = extract_tweet(self.posts)
    #     df_tweet.to_csv(os.path.join(self.path_tweet,'dfcomplete.csv'))
    #     return df_tweet

    def orchestrator(self):
        df_data = self.read_json_dic()
        sentiment_list = sentiment_lists(df_data)
        df_tweet = self.save_df_tweet()
        return df_data, df_tweet


if __name__ == '__main__':
    nlp = Sentimen_Analysis(input='liwc')
    result = nlp.orchestrator()

    
        