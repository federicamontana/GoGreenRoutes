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

from utilities import read_dic, create_emotion_lists, text_emotion, df_byparks, explode, colors, space

class Sentimen_Analysis():
    def __init__(self, input, input_park, input_word, sent, num_lista):
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

        self.park_list = ['ballyhoura','westfields','shannon','arthur']
        self.input_park = input_park
        self.input_word = input_word
        self.sent = sent 
        self.num_lista = num_lista
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
        return df3 #righe le parole, colonne le emozioni, riempimento 1 se corrisponde
    
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
        df.to_csv(os.path.join(self.path_tweet,'df_completec_2.csv'), index = False) 
        return df

    #For each tweet associate a sentiment (2 is that sentiment is present twice)
    #This function is too expensive so we run it once and we saved the result df_final inside dataframe folder
    # def df_join(self,df_dic,df_tweet):
    #     #Apply text_emotion function which return df with the count of ex positive words present in the tweet
    #     df_final = text_emotion(df_tweet, 'text1', df_dic, self.emotions)
    #     #Count the number with emotion in a tweet
    #     df_final['word_em_count'] = df_final[self.emotions].sum(axis=1)
    #     #Devide the number of the ex positive words present in a tweet by the total number of words in the corrispective tweet
    #     return df_final

    #Normalization
    def normalization(self,df_final):
        df_final = pd.read_csv(os.path.join(self.path_tweet,'df_final.csv'))
        df_final['word_em_count'] = df_final[self.emotions].sum(axis=1)
        for emotion in self.emotions:
            df_final[emotion]=df_final[emotion]/df_final['word_em_count']
        return df_final.fillna(0)

    #Analysis
    #df_park sono i df con il nome del parco
    #ds racchiude la statistica 
    #df_media_parks a come colonne i parchi e come righe le emozioni
    def parks_mean(self,df):
        df_media_parks = pd.DataFrame()
        for park in self.park_list:
            df_park, ds = df_byparks(park,df,self.emotions)
            media = ds.loc['mean'].to_list() #media for each emotion
            df_m= pd.DataFrame({park: media}, index = self.emotions)
            df_media_parks = pd.concat([df_media_parks, df_m], axis = 1)
        return df_media_parks, ds
    
    def analysis(self,df,sent_list):
        df_park, ds = df_byparks(self.input_park,df,self.emotions)
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
        plt.savefig(os.path.join(self.path_plot+'/bar_chart/'+name_plot))
        plt.show()
        
    def word_clouds(self, df_count_words, name_plot, sent):
        cmap_plot, color_plot = colors(sent)
        word = dict(zip(df_count_words['result'].tolist(), df_count_words['count'].tolist()))
        # open the twitter image and use np.array to transform the file to an array
        mask = np.array(Image.open("plots/imm/pulcino.png"))
        #create and generate our wordcloud object
        wordcloud_pos = WordCloud(background_color = 'white',
                    contour_color = color_plot,
                    mask = mask, 
                    colormap = cmap_plot,
                    contour_width = 2).generate_from_frequencies(word)
        plt.imshow(wordcloud_pos, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(os.path.join(self.path_plot+'/word_clouds/'+ name_plot))
        plt.show()

    def orchestrator(self):
        df_dic = self.read_json_dic()
        #Creo la lista delle parole associate ai sentimenti
        emotion_lists = create_emotion_lists(df_dic)
        #Read df extracted from Mongodb 
        df1 = pd.read_csv(os.path.join(self.path_tweet,'df_complete_2.csv'))
        df2 = self.text_cleaning(df1) 
        #Read df cleaned directly
        #df_tweet = pd.read_csv(os.path.join(self.path_tweet,'df_completec.csv'))
        #Read df joined directly
        #--df_final = pd.read_csv(os.path.join(self.path_tweet,'df_final.csv'))
        #Normalizzazione
        #--df_norm = self.normalization(df_final)
        
        ####ANALYSIS#####
        #Return the statistics for each parks and the average of the park for each emotion
        #--df_media_parks, ds = self.parks_mean(df_norm)
        #Seleziono le parole corrispondenti alla lista dell'emozione corrispondente
        #--lista = emotion_lists[self.num_lista]
        #Seleziono un parco tramite input_park e conto le parole più frequenti in df_count_words
        #df_match_list: nella colonna 'result' ho le parole che hanno sentiment per ogni tweet
        #--df_count_words, df_match_list = self.analysis(df_norm,lista)
        # self.most_freq_sent_word_bypark(df_count_words,title_plot,name_plot)
        #####CHECK WORDS#####
        #explore_tweet_df contiene solo tweet che hanno 'input_word' selezionata
        #--explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"\b"+self.input_word+r"\b", regex=True)]
        
        #####PLOT#####
        #self.mean_pie(ds,'Pie chart')
        #--self.comparing_parks(df_media_parks,'comparing_parks')
        #--title_plot = 'Most frequent '+self.sent+' words in ' +self.input_park+' park'
        #--self.most_freq_sent_word_bypark(df_count_words,title_plot, self.sent+'_'+self.input_park+'.png')
        #self.word_clouds(df_count_words, 'word_clouds_pos', 'pos')
    
        return df_dic, df2, emotion_lists
        #, explore_tweet_df, df_match_list

park_list = ['ballyhoura','westfields','shannon','arthur']
#0:'affect', 1:'posemo', 2:'negemo', 3:'anx', 4:'anger', 5:'sad',
#6:'social', 7:'family', 8:'friend', 9:'health', 10:'leisure', 11:'death'
if __name__ == '__main__':
    #for park in park_list:
    nlp = Sentimen_Analysis(input ='liwc',input_park = 'westfields', input_word = 'support', 
                            sent = 'negative', num_lista = 2)
    df, df2, el = nlp.orchestrator()
    