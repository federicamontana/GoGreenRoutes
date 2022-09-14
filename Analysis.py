import pandas as pd
import numpy as np 
from nrclex import NRCLex 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from pathlib import Path 
from matplotlib import cm

from Utility_Fede import aggregation_byparks,label,explode
from Sentiment_lists import fear_list, anger_list, trust_list, surprise_list, positive_list, negative_list, sadness_list, disgust_list, joy_list, anticipation_list

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
df = pd.read_csv('dataframe/df_completec.csv')
