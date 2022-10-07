import pandas as pd
import os 
from nltk import word_tokenize
import re
# import spacy
# nlp = spacy.load('en_core_web_sm')
from prova2 import text_emotion
my_path_data = os.path.abspath('')

df_dic = pd.read_csv('Update0/dizionario.csv')
df_tweet = pd.read_csv('dataframe/df_completec.csv')


dfp = pd.DataFrame({"text1": ["Hi abandon abandonig", "abilities", "I have been abuse"]})
df2p = df_dic.head(6).reset_index().drop(['index'],axis=1) #da qua succede il problema
#quello che accade è che emod_score può risultare un dataframe con più righe
# non solo una come dovrebbe e quindi poi quando viene associato a emo_df mi da errore
# ho quindi aggiunto un if in piu per dire che se ottengo un df con piu righe allora 
# prendimi solo la prima riga
#questo anche perchè di solito parole simili hanno anche emozioni uguali e quindi va bene considerare solo una parola
# non si tiene in conto però del fatto che ci sono 2 parole (o piu) e che quindi quel sentimento è associato a 2 (o piu) parole
df = text_emotion(df_tweet, 'text1', df2p)

dfp= df_tweet
df2p = df_dic
emotions = df2p.columns.drop('word')
emo_df = pd.DataFrame(0, index=dfp.index, columns=emotions)
for i,row in dfp.iterrows(): 
    l=[]
    tweet = word_tokenize(dfp.loc[i]['text1'])
    for wt in tweet:
        for word in df2p['word']:
            l.append(bool(re.findall(r"\b"+word,wt)))
        s = pd.Series(l,name = 'word')
        emo_score = df2p[s]
        if len(emo_score) > 1:
            emo_score = emo_score.reset_index().drop(['index'],axis=1).head(1)
        l=[]
        if not emo_score.empty:
            for emotion in emotions:
                emo_df.at[i, emotion] += emo_score[emotion]
df = pd.concat([dfp, emo_df], axis=1)
#Remove i tweet che non hanno associato nessun sentimento
df = df[df[emotions].any(axis=1)]