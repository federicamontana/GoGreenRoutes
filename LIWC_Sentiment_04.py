import pandas as pd
import os
import json
from nltk import tokenize

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

from Read_dictionary_03 import df2_liwc as df
from Read_dictionary_03 import sentiment_list_liwc as sentiment_list
from Read_dictionary_03 import emotions_liwc as emotions
from Utility_Fede_2 import aggregation_byparks_2, text_emotion, explode

#Set index as column and call it 'word'
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'word'})

#Read the tweet dataframe taken from Mongodb and cleaned
tweet_data = pd.read_csv('dataframe/df_completec.csv')
#Select just two columns
tweet_data = tweet_data[['_id','text1']]

#Apply text_emotion function which return df with the count of ex positive words present in the tweet
df_final = text_emotion(tweet_data, 'text1', df)
df_final.head()

#Count words in a tweet
#df_final['word_count_in_tweet'] = df_final['text1'].apply(tokenize.word_tokenize).apply(len)

#Count the number with emotion in a tweet
df_final['word_em_count'] = df_final[emotions].sum(axis=1)
#Devide the number of the ex positive words present in a tweet by the total number of words in the corrispective tweet
for emotion in emotions:
    df_final[emotion]=df_final[emotion]/df_final['word_em_count']
df_final = df_final.fillna(0)


####ANALISI#########

#COMPARISON BETWEEN PARKS
ballyhoura_df,aggr,df_ball = aggregation_byparks_2('ballyhoura',df_final,emotions)
castletroy_df,aggr, df_west = aggregation_byparks_2('castletroy',df_final,emotions)
shannon_df,aggr, df_shannon = aggregation_byparks_2('shannon',df_final,emotions)
arthur_df,aggr, df_ted = aggregation_byparks_2('arthur',df_final,emotions)
df_parks = pd.concat([ballyhoura_df, castletroy_df, shannon_df, arthur_df], axis=1)

#STEP2: Quale parole danno questi sentimenti?
#In Sentiment_lists.py sono presente le liste dei sentimenti pos/neg ecc presi dal vocabolario NRCLex
#Vedo quante parole nel testo pulito text1 sono presenti nella lista e nel parco che scelgo

park_name = 'shannon'
emotion_counting_df,aggr,df_park = aggregation_byparks_2(park_name,df_final,emotions)
#emotional dataframe sorted with most common words
df_em_mc = pd.DataFrame({'emotion': sentiment_list, 'aggregation': aggr}).sort_values(by=['aggregation'],ascending=False)

lista = sentiment_list[2] 
#in df_result sono presente le parole con i conteggi
#df_match_list è il dataframe con la la lista delle parole metchate nella lista sentiemnt
df_result,df_match_list = explode(df_park,lista)
df_result = df_result.reset_index(name="count") # con reset_index mi trasformo la serie in dataframe


#Analisi parole
word = "lose"
#Extract tweet with certain words
#nella colonna result, per ogni riga metto insieme tutte le parole che erano nella lista e vedo se contengono la parola che mi interessa
explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"\b"+word+r"\b", regex=True)]





