import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from PIL import Image
from wordcloud import WordCloud
import seaborn as sns
import numpy as np
import contractions
import spacy
nlp = spacy.load('en_core_web_sm')
import re
stopwords = nlp.Defaults.stop_words

from utilities import read_dic, text_emotion, df_byparks, explode, colors, space

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
        #self.df_tweet = pd.read_csv(os.path.join(self.path_tweet,'df_complete.csv'))

    #Read dictionary  
    def read_json_dic(self) -> pd.DataFrame:
        if self.input == 'liwc':
            dictionary,label = read_dic(self.dict)
            #keylist = list(dictionary.keys())
            #key_cleaned= list(map(lambda x: x.replace('*', ''), keylist))
            with open('dict/liwc_dic.json', 'w') as fp:
                json.dump(dictionary, fp, indent=1)
            dizionario_json = 'dict/liwc_dic.json'
        else:
            dizionario_json = self.dict
        df = pd.read_json(dizionario_json, orient ='index')
        df = df.fillna(0).T.head()
        key_cleaned= list(map(lambda x: x.replace('*', ''), df.columns))
        df = df.set_axis(key_cleaned, axis=1)
        df2 = pd.DataFrame()
        for emotion in self.emotions:
            df2[emotion] = df.apply(lambda i: i.astype(str).str.contains(emotion).any(), axis=0).astype(int)
        #elimino le parole che non hanno associato nessuna delle emozioni scelte
        df3 = df2[df2[self.emotions].any(axis=1)]
        #create sentiment lists (ogni emozione contiene la lista di parole)
        emotion_lists = []
        for i in df2:
            emotion_lists.append(df2.loc[df2[i]!=0][i].reset_index()['index'].tolist())
        return df3, emotion_lists #righe le parole, colonne le emozioni, riempimento 1 se corrisponde
    
    #Text cleaning
    def text_cleaning(self, df):
        # Creation of a new text column called text1 with the first pre-processing step: 
        # Lower case and Expanding Contractions
        df["text1"] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split())).apply(lambda x: contractions.fix(x))
        # Remove hyperlinks
        # Remove websites and email address
        # Remove old style retweet text "rt"
        # Remove punctuations (anche hashtag, @)
        # Remove numbers
        df["text1"] = [re.sub(r"https?:\/\/.\S+|\S+com|\S+@\S+|^rt|[\W_]|\d+", " ", x) for x in  df["text1"]]
        # Remove stopwords
        df["text1"] = df["text1"].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords))
        df['text1'] = df['text1'].apply(space)
        # Creo una colonna con gli Hashtag
        df["hashtag"] = df["text"].apply(lambda x: re.findall(r"#(\w+)", x.lower()))
        df = df.drop_duplicates(subset=['text1'])
        df.to_csv(os.path.join(self.path_tweet,'df_completec.csv'), index = False) 
        return df

    #For each tweet associate a sentiment (2 is that sentiment is present twice)
    def df_join(self,df_dic,df_tweet):
        #Dizionario
        #Set index as column and call it 'word'
        #df_dic = df_dic.reset_index().rename(columns = {'index':'word'})
        #Apply text_emotion function which return df with the count of ex positive words present in the tweet
        df_final = text_emotion(df_tweet, 'text1', df_dic)
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
    def parks_mean(self,df):
        df_media_parks = pd.DataFrame()
        for park in self.park_list:
            df0, ds = df_byparks(park,df,self.emotions)
            media = ds.loc['mean'].to_list()
            df_m= pd.DataFrame({park: media}, index = self.emotions)
            df_media_parks = pd.concat([df_media_parks, df_m], axis = 1)
        return df_media_parks, media
    
    def analysis(self,df_park,sent_list):
        df_count_words, df_match_list = explode(df_park, sent_list)
        return df_count_words, df_match_list
    
    #PLOT
    def mean_pie(self,ds,name_plot):
        plt.pie(ds.loc['mean'].to_list(), labels = self.emotions)
        sns.set(rc={'figure.figsize':(20,10)})
        plt.savefig(os.path.join(self.path_plot,name_plot))
        plt.show()

    def comparing_parks(self,df_media_parks,name_plot):
        cmap = cm.get_cmap('Set3') # Colour map (there are many others)
        df_media_parks.plot.bar(cmap = cmap)
        plt.xlabel("Emotions")
        plt.ylabel("Frequencies")
        plt.savefig(os.path.join(self.path_plot,name_plot))
        plt.show()

    def most_freq_sent_word_bypark(self,df_count_words,title_plot,name_plot):
        plt.figure(figsize=(8,10))
        sns.barplot(y= 'result', x = 'count', data = df_count_words[0:25]) #stampo le prime 25 parole che mi danno sentiment positive
        plt.title(title_plot)
        plt.savefig(os.path.join(self.path_plot,name_plot))
        plt.show()
        
    def word_clouds(self, df_count_words, name_plot, sent):
        cmap_plot, color_plot = colors(sent)
        word = dict(zip(df_count_words['result'].tolist(), df_count_words['count'].tolist()))
        # open the twitter image and use np.array to transform the file to an array
        mask = np.array(Image.open("pulcino.png"))
        #create and generate our wordcloud object
        wordcloud_pos = WordCloud(background_color = 'white',
                    contour_color = color_plot,
                    mask = mask, 
                    colormap = cmap_plot,
                    contour_width = 2).generate_from_frequencies(word)
        plt.imshow(wordcloud_pos, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(os.path.join(self.path_plot,name_plot))
        plt.show()

    def orchestrator(self):
        df_dic, emotion_lists = self.read_json_dic()
        #Read df extracted from Mongodb 
        # df1 = pd.read_csv(os.path.join(self.path_tweet,'df_complete.csv'))
        # df2 = self.text_cleaning(df1) 
        #Read df cleaned
        df_tweet = pd.read_csv(os.path.join(self.path_tweet,'df_completec.csv'))
        df_dic = df_dic.reset_index().rename(columns = {'index':'word'})
        #df_final = self.df_join(df_dic,df_tweet)
        df_final = text_emotion(df_tweet, 'text1', df_dic)
        # df_norm = self.normalization(df_final)
        # ####Analysis#####
        # df_park, ds = df_byparks(self.input_park,df_norm,self.emotions)
        # # df_ball, ds_ball, df_cast, ds_cast, df_shan, ds_shan, df_art, ds_art = self.parks(df_norm)
        # df_media_parks, media = self.parks_mean(df_norm)
        # lista = emotion_lists[2]
        # title_plot = 'titolo'
        # name_plot = 'nome'
        # df_count_words, df_match_list = self.analysis(df_park,lista)
        # self.most_freq_sent_word_bypark(df_count_words,title_plot,name_plot)
        # ####Check words#####
        # #explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"\b"+self.input_word+r"\b", regex=True)]
        # ####Plots#####
        # #self.word_clouds(df_count_words, 'word_clouds', 'pos')
        # self.comparing_parks(df_media_parks,'comparing_parks')
        return df_final


if __name__ == '__main__':
    nlp = Sentimen_Analysis(input='liwc',input_park='shannon', input_word='lose')
    df = nlp.orchestrator()
        