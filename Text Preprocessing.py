import spacy
nlp = spacy.load('en_core_web_sm')
import re #library for regular expressions
import pandas as pd
from collections import Counter
from string import punctuation 
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path 

df = pd.read_csv ('dataframe/df.csv')

### Text cleaning 

# Creation of a new text column called text1 with the first pre-processing step: lower case
df['text1'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['text1'].head()

# Remove hyperlinks
df['text1'] = [re.sub(r'https?:\/\/.\S+', "", x) for x in df['text1']]

# Remove websites and email address
df['text1'] = [re.sub(r"\S+com", "", x) for x in df['text1']]
df['text1'] = [re.sub(r"\S+@\S+", "", x) for x in df['text1']]

# Remove old style retweet text "RT"
df['text1'] = [re.sub(r'^rt[\s]+', '', x) for x in df['text1']]

# Expanding Contractions
# dictionary consisting of the contraction and the actual value
#Questo forse si puo' togliere perchè le contrazioni poi vanno via eliminando le stopwords (vedi dopo)
apos_dict = {"'s":" is","n't":" not","'m":" am","'ll":" will",
           "'d":" would","'ve":" have","'re":" are"}
# replace the contractions
for key,value in apos_dict.items():
    if key in df['text1']:
        df['text1'] = df['text1'].replace(key,value)

# Remove punctuations (anche hashtag, @)
df['text1'] = df['text1'].str.replace('[^\w\s]','')
df['text1'].head()


### Stopwords
# The next step is to remove the useless words, namely, the stopwords. Stopwords are words that frequently appear in many articles,
# but without significant meanings. Examples of stopwords are ‘I’, ‘the’, ‘a’, ‘of’.
# spacy stopwords
stopwords = nlp.Defaults.stop_words
print(len(stopwords)) # 326
print(stopwords)

# exclude the stopwords from the text
df['text1'] = df['text1'].apply(lambda x: " ".join(x for x in x.split() if x not in stopwords))


### Lemmatization
#Another way of converting words to its original form is called stemming.
#Lemmatization is taking a word into its original lemma, and stemming is taking the linguistic root of a word.

# .lemma_ function from spacy 

def space(tweet):
    doc = nlp(tweet)
    return " ".join([token.lemma_ for token in doc])
df['text1'] = df['text1'].apply(space)

## Check which are the most common words
# token dividen
token_ = [i.split() for i in df["text1"]]
# token joined in one list 
#remove words with lenght < 3 and puntctuations !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
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

filepath = Path('../dataframe/dfc.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath) 