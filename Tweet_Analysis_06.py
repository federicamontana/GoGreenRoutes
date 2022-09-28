from turtle import pos
import pandas as pd
import os
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm

from Read_dictionary_03 import df2_liwc as df
from Read_dictionary_03 import sentiment_list_liwc as sentiment_list
from Read_dictionary_03 import emotions_liwc as emotions
from Utility_Fede_2 import aggregation_byparks, text_emotion, explode
from LIWC_Sentiment_04 import df_final

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

park_name = 'ballyhoura'
emotion_counting_df,aggr,df_park = aggregation_byparks(park_name,df_final,emotions)

lista = sentiment_list[0]
df_result,df_match_list = explode(df_park,lista)
df_result = df_result.reset_index(name="count") # con reset_index mi trasformo la serie in dataframe
plt.figure(figsize=(7,7))
sns.barplot(y= 'result', x = 'count', data = df_result[0:25]) #stampo le prime 25 parole che mi danno sentiment positive
plt.title("Most frequent affect words in Ballyhoura park")
#plt.savefig('C:\\Users\\micci\\Desktop\\GoGreenRoutes\\Figures\\Posit_words_west.png')
plt.savefig('/Users/FEDERICA/Desktop/GoGreenRoutes/Figures/affect_words_ball_liwc.png')
plt.show()

word = "miss"
explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"\b"+word+r"\b", regex=True)]


#MOST CITED PARKS
# parks_list = ['shannon', 'ballyhoura','westfields', 'arthur', 'baggot', 'castletroy', 'brein', 'byrne','russel']
# df_result_parks,df_match_list_parks = explode(df,parks_list)
# df_result_parks = df_result_parks.reset_index(name="count") # con reset_index mi trasformo la serie in dataframe
# plt.figure(figsize=(6,6))
# sns.barplot(y= 'result', x = 'count', data = df_result_parks[0:25]) #stampo le prime 25 parole che mi danno sentiment positive
# plt.title("Most cited parks in twitter")
# plt.savefig("Figures/most_cited_parks.png")
# plt.show()

#COMPARISON BETWEEN PARKS
ballyhoura_df,aggr,df_ball = aggregation_byparks('ballyhoura',df_final,emotions)
castletroy_df,aggr, df_west = aggregation_byparks('castletroy',df_final,emotions)
shannon_df,aggr, df_shannon = aggregation_byparks('shannon',df_final,emotions)
arthur_df,aggr, df_ted = aggregation_byparks('arthur',df_final,emotions)
df_parks = pd.concat([ballyhoura_df, castletroy_df, shannon_df, arthur_df], axis=1)
cmap = cm.get_cmap('Set3') # Colour map (there are many others)
df_parks.plot.bar(cmap = cmap)
plt.xlabel("Emotions")
plt.ylabel("Frequencies")
plt.show()
