import pandas as pd
import os
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import seaborn as sns


from Utility_Fede import aggregation_byparks,label,explode
from Sentiment_lists import fear_list, anger_list, trust_list, surprise_list, positive_list, negative_list, sadness_list, disgust_list, joy_list, anticipation_list

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

df = pd.read_csv('dataframe/df_completec.csv')
ballyhoura_df,aggr,df_ball = aggregation_byparks('ballyhoura',df)
westfields_df,aggr, df_west = aggregation_byparks('westfields',df)
shannon_df,aggr, df_shannon = aggregation_byparks('shannon',df)
ted_russel_df,aggr, df_ted = aggregation_byparks('ted russel',df)
#Arthur’s Quay Park
arthur_df,aggr, df_arthur = aggregation_byparks('arthur',df)
baggot_df,aggr, df_baggot = aggregation_byparks('castletroy',df)


lista = negative_list
df_p = df_baggot
df_result,df_match_list = explode(df_p,lista)
df_result = df_result.reset_index(name="count") # con reset_index mi trasformo la serie in dataframe
plt.figure(figsize=(8,10))
sns.barplot(y= 'result', x = 'count', data = df_result[0:25]) #stampo le prime 25 parole che mi danno sentiment positive
plt.title("Most frequent negative words in Ted Russel")
plt.show()
#plt.savefig('/Users/FEDERICA/Desktop/GoGreenRoutes/Figures/negat_words_arthursquay.png')


word = "strike"
explore_tweet_df = df_match_list[df_match_list['result'].apply(lambda x: ' '.join(x)).str.contains(r"^"+word, regex=True)]

