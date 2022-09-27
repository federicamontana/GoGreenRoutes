import spacy
nlp = spacy.load('en_core_web_sm')
import re #library for regular expressions
import pandas as pd
from collections import Counter
from string import punctuation 
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 
import os

os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes')
df = pd.read_csv('dataframe/df_complete.csv')

### Text cleaning 

# Creation of a new text column called text1 with the first pre-processing step: 
# lower case
df['text1'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

# Remove hyperlinks
df['text1'] = [re.sub(r'https?:\/\/.\S+', "", x) for x in df['text1']]

# Remove websites and email address
df['text1'] = [re.sub(r"\S+com", "", x) for x in df['text1']]
df['text1'] = [re.sub(r"\S+@\S+", "", x) for x in df['text1']]

# Remove old style retweet text "RT"
df['text1'] = [re.sub(r'^rt[\s]+', '', x) for x in df['text1']]

#Remove duplicate tweet
df = df.drop_duplicates(subset=['text1']) #rimuove i duplicati 

# Expanding Contractions
# dictionary consisting of the contraction and the actual value
#Questo forse si puo' togliere perchè le contrazioni poi vanno via eliminando le stopwords (vedi dopo)
#TUTTO QUESTO NON FUNZIONA IL METODO REPLACE NON VA BENE, VEDERE MEGLIO USANDO 
#QUALCOSA TIPO
#df['text1'] = df['text1'].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords and x != 'don'))

df['text1'] = df['text1'].apply(lambda x: x.replace("' ", "'"))
df['text1'] = df['text1'].apply(lambda x: x.replace(" '", "'"))
apos_dict = {"'s":" is","n't":" not","'m":" am","'ll":" will",
           "'d":" would","'ve":" have","'re":" are","don't":"do not","don t":"do not","dont":"do not"}
# replace the contractions
for key,value in apos_dict.items():
    if key in df['text1']:
        df['text1'] = df['text1'].str.replace(key,value, inplace=True)

# Remove punctuations (anche hashtag, @)
df['text1'] =[re.sub("[\W_]", ' ', x) for x in df['text1']]

# Remove numbers
df['text1'] =[re.sub("\d+", "", x) for x in df['text1']]
#Remove don che deriva da don't ma ha un significato nel vocabolario
#df['text1'] =[re.sub("\badare\b", "", x) for x in df['text1']]

### Stopwords
# The next step is to remove the useless words, namely, the stopwords. Stopwords are words that frequently appear in many articles,
# but without significant meanings. Examples of stopwords are ‘I’, ‘the’, ‘a’, ‘of’.
# spacy stopwords
stopwords = nlp.Defaults.stop_words
#print(len(stopwords)) # 326
#print(stopwords)
# exclude the stopwords from the text
df['text1'] = df['text1'].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords and x != 'don'))


### Lemmatization
#Another way of converting words to its original form is called stemming.
#Lemmatization is taking a word into its original lemma, and stemming is taking the linguistic root of a word.
# .lemma_ function from spacy 
def space(tweet):
    doc = nlp(tweet)
    return " ".join([token.lemma_ for token in doc])
df['text1'] = df['text1'].apply(space)

df.to_csv('dataframe/df_completec.csv') 

#FINE PULIZIA

########################################################
## Check which are the most common words
# token dividen
token_ = [i.split() for i in df["text1"]]
#token joined in one list 
#remove words with lenght < 3 and puntctuations !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#remove the word 'don' which derive from 'don't' but has a meaning in the vocabolary (like Don Name)
tokens = [item for sublist in token_ for item in sublist if len(item) > 3 and item not in punctuation]

# Print most common word
n_print = int(input("How many most common words to print: "))
print("\nOK. The {} most common words are as follows\n".format(n_print))
word_counter = Counter(tokens)
for word, count in word_counter.most_common(n_print):
    print(word, ": ", count)

# Create a data frame of the most common words 
lst = word_counter.most_common(n_print)
df_most_common = pd.DataFrame(lst, columns = ['Word', 'Count'])

# Draw a bar chart dropping limerick 
plt.figure(figsize=(8,10))
sns.barplot(y= 'Word', x = 'Count', data = df_most_common.drop([0,1]))
plt.show()

