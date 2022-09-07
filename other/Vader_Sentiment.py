### Using VADER lexicon for SA with nltk ###
# VADER ( Valence Aware Dictionary for Sentiment Reasoning) is a model used for text sentiment analysis that is sensitive to both polarity (positive/negative) 
# and intensity (strength) of emotion. 
# It is available in the NLTK package and can be applied directly to unlabeled text data.

import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser' # devo fare il render nel browser perchè in spyder non si aprono i plot
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
SIA = SentimentIntensityAnalyzer()


df['text1'] = df['text1'].astype(str)

# Applying Model, Variable Creation
df['Polarity Score'] = df['text1'].apply(lambda x:SIA.polarity_scores(x)['compound'])
df['Neutral Score'] = df['text1'].apply(lambda x:SIA.polarity_scores(x)['neu'])
df['Negative Score'] = df['text1'].apply(lambda x:SIA.polarity_scores(x)['neg'])
df['Positive Score'] = df['text1'].apply(lambda x:SIA.polarity_scores(x)['pos'])

# Converting 0 to 1 Decimal Score to a Categorical Variable
df['Sentiment']=''
df.loc[df['Polarity Score'] >0,'Sentiment']='Positive'
df.loc[df['Polarity Score'] == 0,'Sentiment']='Neutral'
df.loc[df['Polarity Score'] <0,'Sentiment']='Negative'
df[:5]

count = df["Sentiment"].value_counts()
# Positive    626
# Neutral     386
# Negative     90

# Plot it
VADERsent_df = pd.DataFrame.from_dict(count)
VADERsent_df = VADERsent_df.reset_index()
VADERsent_df = VADERsent_df.rename(columns={'index' : 'Sentiment value' , "Sentiment": 'Sentiment count'})
VADER_fig = px.bar(VADERsent_df, x='Sentiment count', y='Sentiment value', color = 'Sentiment value', orientation='h',
             width = 800, height = 400, color_discrete_sequence=px.colors.qualitative.Set3)
VADER_fig.show()

pol_score = px.line(df_green, x="text1", y="Polarity Score")
pol_score.show()

### NRC Word-Emotion Association Lexicon (aka EmoLex) ###
# The NRC Word-Emotion Association Lexicon (often shortened to NRC Emotion Lexicon, and originally called EmoLex) 
# is a list of English words and their manually annotated associations with eight basic emotions (anger, fear, anticipation, trust, surprise, sadness, joy, and disgust) 
# and two sentiments (negative and positive). Translations of the lexicon in other languages are available.

## LeXmo package
emo = df['text1'].apply(lambda x:LeXmo.LeXmo(x))

# NRC Word-Emotion Association Lexicon without package but importing the .txt file
filepath = "C:/Users/micci/Downloads/NRC-Suite-of-Sentiment-Emotion-Lexicons/NRC-Suite-of-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t')
emolex_df.head(12)

###### creation of a column where I convert the tweets in list of words # NON USATO
#df_green["token"] = [i.split() for i in df_green["text1"]]

## USING NRClex 
## Is based on the National Research Council Canada (NRC) affect lexicon 
# and the NLTK library's WordNet synonym sets

print(df['text1'].astype('string'))

# Since our data frame contains separate tweet strings, 
# we will join them to create a string object containing all of our tweets
str_tweet = ",".join(df["text1"])
str_tweet = str_tweet.split()

# Remove the duplicates (Ha senso?)
str_tweet = list(set(str_tweet))


# Let's for ex calculate the frequencies
for i in range(len(str_tweet)):
    text_object = NRCLex(str_tweet[i])
    print("\n\n", str_tweet[i], ": ", text_object.affect_frequencies)

## We can now extract from the origianl EmoLex dictionary one dictionary with just our words

# Uploading the emolex dictionary
filepath = "C:/Users/micci/Downloads/NRC-Suite-of-Sentiment-Emotion-Lexicons/NRC-Suite-of-Sentiment-Emotion-Lexicons/NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t')
emolex_df

# creation of the new dictionary
my_emolex = emolex_df[emolex_df["word"].isin(str_tweet)]

# How many words does each emotion have? 
em_count = my_emolex[my_emolex.association == 1].emotion.value_counts()
em_count

# plot it
labels = ["positive", "trust", "negative", "anticipation", "joy", "fear", "anger", "surprise", "sadness", "disgust"]
mycolors = ["AliceBlue", "Aquamarine", "Coral", "LightGreen", "LightSkyBlue", "Violet", "Teal", "Tomato", "PapayaWhip", "Khaki"]
plt.pie(em_count, labels = labels, colors = mycolors)

# I want to see the anticipation words
my_emolex[(my_emolex.association == 1) & (my_emolex.emotion == 'anticipation')]
 
