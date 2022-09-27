import pandas as pd
from nrclex import NRCLex 
import numpy as np

from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from tqdm.notebook import tqdm as tqdm
#from tqdm import tqdm_notebook as tqdm
from tqdm import trange

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
    #.drop_duplicates(subset=['text1'])  #rimuove stessi tweet ma l ho messo nel file di pulizia
    aggr = [] #lista che contiene le medie
    for i in df_f['emotions_freq'].apply(pd.Series).drop("anticip", axis=1) : aggregation(i,df_s,aggr)
    df_park= pd.DataFrame({park: aggr}, index = label)
    return df_park, aggr, df_s

def aggregation_byparks_raw(park,df):
    df = df[df['text1'].str.contains(park)] #cerco i tweet che hanno quel parco all'interno del testo
    df_f = pd.DataFrame(df['text1'])
    df_f["emotions_freq"] = df_f["text1"].apply(lambda x: NRCLex(x).raw_emotion_scores) #Return affect frequencies
    #Concateno il dataframe df_f in cui ho preso solo la colonna text1 con drop
    # e quello in cui ho estratto il dizionario in formato pandas e messo le emozioni in colonna
    #con .drop elimino la colonna anticip che è in più dato che esiste anticipation
    df_s = pd.concat([df_f.drop(['emotions_freq'], axis = 1), df_f['emotions_freq'].apply(pd.Series)], axis = 1)
    df_s = df_s.replace(np.nan,0) #Replace NaN with 0 
    #.drop_duplicates(subset=['text1'])  #rimuove stessi tweet ma l ho messo nel file di pulizia
    aggr = [] #lista che contiene le medie
    for i in df_f['emotions_freq'].apply(pd.Series): aggregation(i,df_s,aggr)
    df_park= pd.DataFrame({park: aggr}, index = label)
    return df_park, aggr, df_s
    
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


#LETTURA .dic
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


def text_emotion(df, column, df3):
    '''
    INPUT: DataFrame, string
    OUTPUT: the original DataFrame with ten new columns for each emotion
    '''

    new_df = df.copy()

    emotions = df3.columns.drop('word')
    emo_df = pd.DataFrame(0, index=df.index, columns=emotions)

    stemmer = SnowballStemmer("english")

    
    with tqdm(total=len(list(new_df.iterrows()))) as pbar:
        for i, row in new_df.iterrows():
            pbar.update(1)
            document = word_tokenize(new_df.loc[i][column])
            for word in document:
                word = stemmer.stem(word.lower())
                emo_score = df3[df3.word == word]
                if not emo_score.empty:
                    for emotion in list(emotions):
                        emo_df.at[i, emotion] += emo_score[emotion]

    new_df = pd.concat([new_df, emo_df], axis=1)

    return new_df

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
