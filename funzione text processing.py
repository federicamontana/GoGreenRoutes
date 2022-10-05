import spacy
nlp = spacy.load('en_core_web_sm')
import re #library for regular expressions
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
import contractions
import os
stopwords = nlp.Defaults.stop_words

# Funzione per la pulizia dei tweet
path_tweet = os.path.abspath('dataframe')
df = pd.read_csv(os.path.join(path_tweet,'df_complete.csv'))

def text_cleaning(text):
        # Expanding Contractions
        df["text1"] = df["text1"].apply(lambda x: contractions.fix(x))
        # Creation of a new text column called text1 with the first pre-processing step: 
        # Lower case and Expanding Contractions
        df["text1"] = text.apply(lambda x: " ".join(x.lower() for x in x.split())).apply(lambda x: contractions.fix(x))
        # Remove hyperlinks
        # Remove websites and email address
        # Remove old style retweet text "rt"
        # Remove punctuations (anche hashtag, @)
        # Remove numbers
        df["text1"] = [re.sub(r"https?:\/\/.\S+|\S+com|\S+@\S+|^rt|[\W_]|\d+", " ", x) for x in  df["text1"]]
        # Remove stopwords
        df["text1"] = df["text1"].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords))

        return df["text1"]

# Funzione per lemmanization

def space(tweet):
    doc = nlp(tweet)
    return " ".join([token.lemma_ for token in doc])



# text cleaning
df["text1"] = text_cleaning(df["text"])
# text lemmanization
df['text1'] = df['text1'].apply(space)
#Remove duplicate tweet with the same text
df = df.drop_duplicates(subset=['text1'])

# Creo una colonna con gli Hashtag
df["hashtag"] = df["text"].apply(lambda x: re.findall(r"#(\w+)", x.lower()))


df.to_csv('dataframe/df_completec.csv') 



### PULIZIA LIWC
dict = open('dict/liwc_dic.json')
dict_l = json.load(dict)
keylist = list(dict_l.keys())
key_cleaned= list(map(lambda x: x.replace('*', ''), keylist))

dict = pd.read_csv("dict/df_liwc.csv")
dict = dict.drop(dict.columns[0], axis=1)
dict= dict.set_axis(key_cleaned, axis=1)
# trasformo df in dizionario
liwc_json = {col: list(dict[col]) for col in dict.columns}
