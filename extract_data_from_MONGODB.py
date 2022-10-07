from importlib.resources import path
from pymongo import MongoClient
import pprint
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import os 
import socket

filepath = os.path.abspath('')
output_path = os.path.abspath('dataframe')

# Credentials to access Mongo DB
client = MongoClient('localhost', 27018)
db = client['ggr']
posts = db['limerick.posts']

# Df with 
df_green = pd.DataFrame(posts.find({"$and" : 
                                               [{"$text":{"$search": "shannon nature ballyhoura Thomond Park Westfields peoplespark TedRussell Adare Wetlands shelbourne arthur castletroy"}},
                                                {"geo": {"place_id": "54e862bb3ff2f749"}}]} )) # 1102 post
df_green1 = pd.DataFrame(posts.find({ "$text":{"$search": "\"shannon estuary\" \"limerick\""}} )) # 345
df_green1_2 = pd.DataFrame(posts.find({ "$text":{"$search": "\"shannon river\" \"limerick\""}} )) # 776
df_green2 = pd.DataFrame(posts.find({ "$text":{"$search": "\"park\" \"limerick\""}} )) # 20595
df_green3 = pd.DataFrame(posts.find({ "$text":{"$search": "\"ballyhoura\" \"limerick\""}} )) # 1866
df_green4 = pd.DataFrame(posts.find({ "$text":{"$search": "\"westfields\" \"limerick\""}} )) # 666
df_green5 = pd.DataFrame(posts.find({ "$text":{"$search": "\"ted russel\" \"limerick\""}} )) # 69
df_green6 = pd.DataFrame(posts.find({ "$text":{"$search": "\"nature\" \"limerick\""}} )) # 2381
df_green7 = pd.DataFrame(posts.find({ "$text":{"$search": "\"arthur's park\" \"limerick\""}} )) 
df_green8 = pd.DataFrame(posts.find({ "$text":{"$search": "\"castletroy\" \"limerick\""}} )) 

df = pd.concat([df_green, df_green1, df_green1_2,  
                         df_green2, df_green3, df_green4, df_green5, df_green6, df_green7, df_green8 ]).drop_duplicates(subset = ["id"]).reset_index(drop=True) # 26896

df.to_csv(os.path.join(output_path,'df_complete.csv'), index = False)

