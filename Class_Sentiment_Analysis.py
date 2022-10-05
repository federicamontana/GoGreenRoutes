import pandas as pd
import os
import json

from pymongo import MongoClient
from utilities import read_dic, text_emotion, df_byparks, explode

#df = pd.read_csv(os.path.join(self.path_tweet,'dfcompletec.csv'))

class Sentimen_Analysis():
    def __init__(self, input, input_park, input_word):
        #path
        self.path_data = os.path.abspath('dict')
        self.path_tweet = os.path.abspath('dataframe')
        self.path_plot = os.path.abspath('plots')
        #input vocabulary
        self.input = input
        if self.input == 'liwc':
            self.dict = 'dict/LIWC2007_English080730.dic'
            self.emotions = ['affect','posemo','negemo','anx','anger','sad',
            'social','family','friend','health','leisure','death'] 
        else:
            self.dict = 'dict/nrc_en.json'
            self.emotions =['fear', 'anger','trust','surprise','positive',
            'negative','sadness','disgust','joy','anticipation']

        self.park_list = ['ballyhoura','castletroy','shannon','arthur']
        self.input_park = input_park
        self.input_word = input_word

    #Read dictionary  
    def read_json_dic(self) -> pd.DataFrame:
        if self.input == 'liwc':
            dictionary,label = read_dic(self.dict)
            #words = list(dictionary.keys())

            with open('dict/liwc_dic.json', 'w') as fp:
                json.dump(dictionary, fp, indent=1)
            dizionario_json = 'dict/liwc_dic.json'
        else:
            dizionario_json = self.dict
        df = pd.read_json(dizionario_json, orient ='index')
        df = df.fillna(0).T.head()
        df2 = pd.DataFrame()
        for emotion in self.emotions:
            df2[emotion] = df.apply(lambda i: i.astype(str).str.contains(emotion).any(), axis=0).astype(int)
        #create sentiment lists (ogni emozione contiene la lista di parole)
        emotion_lists = []
        for i in df2:
            emotion_lists.append(df2.loc[df2[i]!=0][i].reset_index()['index'].tolist())
        return df2, emotion_lists #righe le parole, colonne le emozioni, riempimento 1 se corrisponde

    #For each tweet associate a sentiment (2 is that sentiment is present twice)
    def compare_df(self,df):
        #Dizionario
        #Set index as column and call it 'word'
        df = df.reset_index().rename(columns = {'index':'word'})
        #Tweet - DA MODIFICARE
        df2 = pd.read_csv(os.path.join(self.path_tweet,'df_completec.csv'))[['text1']]
        #Apply text_emotion function which return df with the count of ex positive words present in the tweet
        df_final = text_emotion(df2, 'text1', df)
        #Count the number with emotion in a tweet
        df_final['word_em_count'] = df_final[self.emotions].sum(axis=1)
        #Devide the number of the ex positive words present in a tweet by the total number of words in the corrispective tweet
        return df_final

    #Normalization
    def normalization(self,df_final):
        for emotion in self.emotions:
            df_final[emotion]=df_final[emotion]/df_final['word_em_count']
        return df_final.fillna(0)

    #Analysis
    #NB arthur ha un problema, sembra che non ci sia 

    # def parks(self,df):
    #     df, ds = df_byparks(self.input_park,df,self.emotions)
    #     #df_ball, ds_ball = df_byparks(self.park_list[0],df,self.emotions)
    #     #df_cast, ds_cast = df_byparks(self.park_list[1],df,self.emotions)
    #     #df_shan, ds_shan = df_byparks(self.park_list[2],df,self.emotions)
    #     #df_art, ds_art = df_byparks(self.park_list[3],df,self.emotions)
    #     #return df_ball, ds_ball, df_cast, ds_cast, df_shan, ds_shan, df_art, ds_art
    #     return df, ds

    def parks_mean(self,df):
        df_media_parks = pd.DataFrame()
        for park in self.park_list:
            df0, ds = df_byparks(park,df,self.emotions)
            media = ds.loc['mean'].to_list()
            df_m= pd.DataFrame({park: media}, index = self.emotions)
            df_media_parks = pd.concat([df_media_parks, df_m], axis =1)
        return df_media_parks
    
    def analysis(self,df_park,sent_list):
        df_count_words, df_match_list = explode(df_park, sent_list)
        return df_count_words, df_match_list
    
    #PLOT


    def orchestrator(self):
        df_dic, sl = self.read_json_dic()
        df_final = self.compare_df(df_dic)
        df_norm = self.normalization(df_final)
        df_park, ds = df_byparks(self.input_park,df_norm,self.emotions)
        # df_ball, ds_ball, df_cast, ds_cast, df_shan, ds_shan, df_art, ds_art = self.parks(df_norm)
        # df_media_park = self.parks_mean(df_norm)
        lista = sl[2]
        df_count_words, df_match_list = self.analysis(df_park,lista)
        #Analysis words
        explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"\b"+self.input_word+r"\b", regex=True)]
        return df_match_list, explore_tweet_df


if __name__ == '__main__':
    nlp = Sentimen_Analysis(input='liwc',input_park='shannon', input_word='lose')
    df1,df2 = nlp.orchestrator()

    
        