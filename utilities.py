import pandas as pd
from nrclex import NRCLex 
import numpy as np
import json
import os 

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')

#READ both JSON and .DIC FILES
#dict_json,dict_dic,emotions_nrc,emotions_liwc,inpu
# def read_json_dic(dict_json,dict_dic,emotions_nrc,emotions_liwc,input):
#     if input == 'liwc':
#         emotions = emotions_liwc
#         dictionary,label = read_dic(dict_dic)
#         words = list(dictionary.keys())

#         with open('dict/liwc_dic.json', 'w') as fp:
#             json.dump(dictionary, fp, indent=1)
#         dizionario_json = 'dict/liwc_dic.json'
#     else:
#         dizionario_json = dict_json
#         emotions = emotions_nrc
#     df = pd.read_json(dizionario_json, orient ='index')
#     df = df.fillna(0).T.head()
#     df2 = pd.DataFrame()
#     for emotion in emotions:
#         df2[emotion] = df.apply(lambda i: i.astype(str).str.contains(emotion).any(), axis=0).astype(int)
#     return df2

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

#CREATE SENTIMENT LIST
def sentiment_lists(df):
    sentiment_list= []
    for i in df: 
        sentiment_list.append(df.loc[df[i]!=0][i].reset_index()['index'].tolist())
    return sentiment_list