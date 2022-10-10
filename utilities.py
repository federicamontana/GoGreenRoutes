import pandas as pd
from nrclex import NRCLex 
import numpy as np
import os 
import matplotlib as mpl
from matplotlib import cm
from nltk import word_tokenize
import spacy
nlp = spacy.load('en_core_web_sm')
import re

filepath = os.path.abspath('')
output_path = os.path.abspath('dict')
#READ .dic
def _parse_categories(lines):
    """
    Read (category_id, category_name) pairs from the categories section.
    Each line consists of an integer followed a tab and then the category name.
    This section is separated from the lexicon by a line consisting of a single "%".
    """
    for line in lines:
        line = line.strip()
        if line == "%":
            return
        # ignore non-matching groups of categories
        if "\t" in line:
            category_id, category_name = line.split("\t", 1)
            yield category_id, category_name

def _parse_lexicon(lines, category_mapping):
    """
    Read (match_expression, category_names) pairs from the lexicon section.
    Each line consists of a match expression followed by a tab and then one or more
    tab-separated integers, which are mapped to category names using `category_mapping`.
    """
    for line in lines:
        line = line.strip()
        parts = line.split("\t")
        yield parts[0], [category_mapping[category_id] for category_id in parts[1:]]

def read_dic(filepath):
    """
    Reads a LIWC lexicon from a file in the .dic format, returning a tuple of
    (lexicon, category_names), where:
    * `lexicon` is a dict mapping string patterns to lists of category names
    * `category_names` is a list of category names (as strings)
    """
    with open(filepath) as lines:
        # read up to first "%" (should be very first line of file)
        for line in lines:
            if line.strip() == "%":
                break
        # read categories (a mapping from integer string to category name)
        category_mapping = dict(_parse_categories(lines))
        # read lexicon (a mapping from matching string to a list of category names)
        lexicon = dict(_parse_lexicon(lines, category_mapping))
    return lexicon, list(category_mapping.values())
    #return dizionario
#####################################
#Create emotion lists
def create_emotion_lists(df):
    emotion_lists = []
    for i in df:
        emotion_lists.append(df.loc[df[i]!=0][i].reset_index()['index'].tolist())
    return emotion_lists 
####################################
# Funzione per lemmanization

def space(tweet):
    doc = nlp(tweet)
    return " ".join([token.lemma_ for token in doc])
###########################################
#CREATE SENTIMENT LIST
def sentiment_lists(df):
    sentiment_list= []
    for i in df: 
        sentiment_list.append(df.loc[df[i]!=0][i].reset_index()['index'].tolist())
    return sentiment_list

########################################################

#Return df with the count of es. positive words present in the tweet
def text_emotion0(df_tweet, column, df_dic, emotions):
    #df : contiene i tweet
    #df3 : vocabolario
    '''
    INPUT: DataFrame, string
    OUTPUT: the original DataFrame with ten new columns for each emotion
    '''
    df = df_tweet.copy()
    #Set index as column and call it 'word'
    df_dic = df_dic.reset_index().rename(columns = {'index':'word'})
    #emotions = df_dic.columns.drop('word')
    emo_df = pd.DataFrame(0, index=df.index, columns=emotions)
    for i,row in df.iterrows(): 
        l=[]
        tweet = word_tokenize(df.loc[i][column])
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
        tweet = word_tokenize(df.loc[i][column])
        for wt in tweet:
            for word in df_dic['word']:
                l.append(bool(re.findall(r"\b"+word,wt)))
            s = pd.Series(l,name = 'word')
            emo_score = df_dic[s]
            if len(emo_score) > 1:
                emo_score = emo_score.reset_index().drop(['index'],axis=1).head(1)
            l=[]
            if not emo_score.empty:
                for emotion in emotions:
                    emo_df.at[i, emotion] += emo_score[emotion]
    df = pd.concat([df, emo_df], axis=1)
    #Remove i tweet che non hanno associato nessun sentimento
    df = df[df[emotions].any(axis=1)]
    return df

#######################################################################
#########################ANALYSIS########################

#Mi prende il df del parco che mi interessa e mi calcola la statistica 
def df_byparks(park,df,emotions):
    df_park = df[df['text1'].str.contains(park)] #cerco i tweet che hanno quel parco all'interno del testo
    ds = df_park[emotions].describe()
    #inserire questa linea se voglio il mean sentiment counting di ogni parco 
    #df_park= pd.DataFrame({park: aggr}, index = emotions)
    #emotional dataframe sorted with most common words
    #df_em_mc = pd.DataFrame({'emotion': sentiment_list, 'aggregation': aggr}).sort_values(by=['aggregation'],ascending=False)
    return df_park, ds

#Find words in tweet which are in sentiment_lists
def find_values(x,sent_list):
    results = []
    for value in sent_list:
        for word in x.split():
            if word == value:
                results.append(word)
    return results

def explode(df,sent_list):
    #inserisco nella colonna result le parole dei tweet che si trovano nella lista
    df['result'] = df['text1'].apply(lambda x: find_values(x,sent_list))
    #elimino le righe in cui la colonna è vuota (perchè non ha trovato niente)
    df_match_list = df[df['result'].map(lambda d: len(d)) > 0]
    df_result = df_match_list.explode("result").groupby(by="result")["result"].count().sort_values(ascending=False)
    return df_result.reset_index(name="count"), df_match_list

def colors(sent):
    # import the desired colormap from matplotlib
    if sent == 'pos':
        cmap = mpl.cm.Blues(np.linspace(0,1,20)) 
        # the darker part of the matrix is selected for readability
        cmap = mpl.colors.ListedColormap(cmap[-10:,:-1]) 
        color = 'lightblue'
    else:
        cmap = mpl.cm.Reds(np.linspace(0,1,20)) 
        cmap = mpl.colors.ListedColormap(cmap[-10:,:-1]) 
        color = 'red'
    return cmap, color


