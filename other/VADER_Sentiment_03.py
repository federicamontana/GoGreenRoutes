import pandas as pd
from nltk import tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import os

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
#os.chdir("C:\\Users\\micci\\Desktop\\GoGreenRoutes")

#https://github.com/svdeepak99/TSA-Twitter_Sentiment_Analysis
analyzer = SentimentIntensityAnalyzer()
sentiments_list = list()
