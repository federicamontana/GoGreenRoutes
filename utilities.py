import pandas as pd
from nrclex import NRCLex 
import numpy as np
import json
import os 
from pymongo import MongoClient
from pathlib import Path

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

#CREATE SENTIMENT LIST
def sentiment_lists(df):
    sentiment_list= []
    for i in df: 
        sentiment_list.append(df.loc[df[i]!=0][i].reset_index()['index'].tolist())
    return sentiment_list

#Extract data from MONGODB
# def extract_tweet(posts):
#     # Df with 
#     df_green = pd.DataFrame(posts.find({"$and" : 
#                                                 [{"$text":{"$search": "shannon nature ballyhoura Thomond Park Westfields peoplespark TedRussell Adare Wetlands shelbourne"}},
#                                                     {"geo": {"place_id": "54e862bb3ff2f749"}}]} )) # 1102 post
#     df_green1 = pd.DataFrame(posts.find({ "$text":{"$search": "\"shannon estuary\" \"limerick\""}} )) # 345
#     df_green1_2 = pd.DataFrame(posts.find({ "$text":{"$search": "\"shannon river\" \"limerick\""}} )) # 776
#     df_green2 = pd.DataFrame(posts.find({ "$text":{"$search": "\"park\" \"limerick\""}} )) # 20595
#     df_green3 = pd.DataFrame(posts.find({ "$text":{"$search": "\"ballyhoura\" \"limerick\""}} )) # 1866
#     df_green4 = pd.DataFrame(posts.find({ "$text":{"$search": "\"westfields\" \"limerick\""}} )) # 666
#     df_green5 = pd.DataFrame(posts.find({ "$text":{"$search": "\"ted russel\" \"limerick\""}} )) # 69
#     df_green6 = pd.DataFrame(posts.find({ "$text":{"$search": "\"nature\" \"limerick\""}} )) # 2381

#     df = pd.concat([df_green, df_green1, df_green1_2,  
#                             df_green2, df_green3, df_green4, df_green5, df_green6 ]).drop_duplicates(subset = ["id"]).reset_index(drop=True) # 26896
#     df.to_csv(os.path.join(output_path,'dfcomplete.csv'))
#     return df