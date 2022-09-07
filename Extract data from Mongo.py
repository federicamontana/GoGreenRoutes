from pymongo import MongoClient
import pprint
import pandas as pd
from pandas import DatclearaFrame

# Credentials to access Mongo DB
client = MongoClient('localhost', 27018)
db = client['ggr']

places = db['limerick.places']
users = db['limerick.users']
media = db['limerick.media']
posts = db['limerick.posts']

# To get more than a single document as the result of a query we use the find() method
for post in places.find():
    pprint.pprint(post)

# If we just want to know how many documents match a query we can perform a count_documents()
places.count_documents({"name": "Limerick"}) # 6
places.count_documents({"country": "Irlanda"}) # 1314

### Indexing (Gia fatto da Rossano)
# MongoDB provides a text index type that supports searching for string content in a collection.
# Indexes can improve the efficiency of read operations. 

posts.index_information() # to know which index are present

posts.find({"$text":{"$search":"nature"}}) # return a Cursor  -> transform it in a list
nature = posts.find({"$text":{"$search":"ilovelimerick"}})
nature_list = list(nature) # 31301
limerick = posts.find({"$text":{"$search":"limerick"}})
limerick_list = list(limerick) #979143



# Df with 
df_green = pd.DataFrame(posts.find({"$and" : 
                                               [{"$text":{"$search": "shannon nature ballyhoura Thomond Park Westfields peoplespark TedRussell Adare Wetlands shelbourne"}},
                                                {"geo": {"place_id": "54e862bb3ff2f749"}}]} )) # 1102 post
df_green1 = pd.DataFrame(posts.find({ "$text":{"$search": "\"shannon estuary\" \"limerick\""}} )) # 345
df_green1_2 = pd.DataFrame(posts.find({ "$text":{"$search": "\"shannon river\" \"limerick\""}} )) # 776
df_green2 = pd.DataFrame(posts.find({ "$text":{"$search": "\"park\" \"limerick\""}} )) # 20595
df_green3 = pd.DataFrame(posts.find({ "$text":{"$search": "\"ballyhoura\" \"limerick\""}} )) # 1866
df_green4 = pd.DataFrame(posts.find({ "$text":{"$search": "\"westfields\" \"limerick\""}} )) # 666
df_green5 = pd.DataFrame(posts.find({ "$text":{"$search": "\"ted russel\" \"limerick\""}} )) # 69
df_green6 = pd.DataFrame(posts.find({ "$text":{"$search": "\"nature\" \"limerick\""}} )) # 2381

df = pd.concat([df_green, df_green1, df_green1_2,  
                         df_green2, df_green3, df_green4, df_green5, df_green6 ]).drop_duplicates(subset = ["id"]).reset_index(drop=True) # 26896


