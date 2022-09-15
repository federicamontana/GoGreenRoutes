import pandas as pd
import numpy as np 
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os
import sys
from pathlib import Path 
from matplotlib import cm
from PIL import Image
from wordcloud import WordCloud
os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
from Utility_Fede import aggregation_byparks,label,explode
from Sentiment_lists import fear_list, anger_list, trust_list, surprise_list, positive_list, negative_list, sadness_list, disgust_list, joy_list, anticipation_list
from NRC_Sentiment import aggr,df_em_mc,df_parks,df_result


#Pie chart of verage sentiment in a park (Ballyouhura)
plt.pie(aggr, labels = label) #, autopct='%.0f%%'
sns.set(rc={'figure.figsize':(20,10)})
plt.show()

#Bar plot
plt.figure(figsize=(8,10))
sns.barplot(y = 'emotion', x= 'aggregation', data = df_em_mc)
plt.show()

#Comparing 4 parks
cmap = cm.get_cmap('Set3') # Colour map (there are many others)
df_parks.plot.bar(cmap = cmap)
plt.xlabel("Emotions")
plt.ylabel("Frequencies")
plt.show()

#Most frequent postive words in Ballyohurara park (change lista to have other sentiment)
plt.figure(figsize=(8,10))
sns.barplot(y= 'result', x = 'count', data = df_result[0:25]) #stampo le prime 25 parole che mi danno sentiment positive
plt.show()

#WordCloud Positive Ballyhoura
word_pos = dict(zip(df_result['result'].tolist(), df_result['count'].tolist()))
# open the twitter image and use np.array to transform the file to an array
mask = np.array(Image.open("imm/pulcino.png"))
# import the desired colormap from matplotlib
cmap1 = mpl.cm.Blues(np.linspace(0,1,20)) 
cmap2 = mpl.cm.Reds(np.linspace(0,1,20)) 

# the darker part of the matrix is selected for readability
cmap1 = mpl.colors.ListedColormap(cmap1[-10:,:-1]) 
cmap2 = mpl.colors.ListedColormap(cmap2[-10:,:-1]) 

color1 = 'lightblue'
color2 = 'red'
#create and generate our wordcloud object
wordcloud_pos = WordCloud(background_color = 'white',
                      contour_color = color1,
                      mask = mask, 
                      colormap = cmap1,
                      contour_width = 2).generate_from_frequencies(word_pos)


#plot
plt.imshow(wordcloud_pos, interpolation='bilinear')
plt.axis('off')
plt.show()

#WordCloud Negative Ballyhoura
