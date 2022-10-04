import spacy
nlp = spacy.load('en_core_web_sm')
import re #library for regular expressions
import pandas as pd
from collections import Counter
from string import punctuation 
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
import contractions
import os


# Funzione per la pulizia dei tweet


def text_cleaning(text):
        # Creation of a new text column called text1 with the first pre-processing step: 
        # lower case
        df["text1"] = text.apply(lambda x: " ".join(x.lower() for x in x.split()))
        # Remove hyperlinks
        df["text1"] = [re.sub(r'https?:\/\/.\S+', "", x) for x in  df["text1"]]
        # Remove websites and email address
        df["text1"] = [re.sub(r"\S+com", "", x) for x in df["text1"]]
        df["text1"] = [re.sub(r"\S+@\S+", "", x) for x in df["text1"]]
        # Remove old style retweet text "rt"
        df["text1"] = [re.sub(r'rt', '', x) for x in df["text1"]]
        # Expanding Contractions
        df["text1"] = df["text1"].apply(lambda x: contractions.fix(x))
        # Remove punctuations (anche hashtag, @)
        df["text1"] = [re.sub("[\W_]", ' ', x) for x in df["text1"]]
        # Remove numbers
        df["text1"] = [re.sub("\d+", "", x) for x in df["text1"]]
        # Remove stopwords
        df["text1"] = df["text1"].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords and x != 'don'))

        return df["text1"]



# Funzione per lemmanization

def space(tweet):
    doc = nlp(tweet)
    return " ".join([token.lemma_ for token in doc])



# text cleaning
df["text1"] = text_cleaning(df["text"])
# text lemmanization
df['text1'] = df['text1'].apply(space)

# Creo una colonna con gli Hashtag
df["hashtag"] = df["text"].apply(lambda x: re.findall(r"#(\w+)", x.lower()))


df.to_csv('dataframe/df_completec.csv') 