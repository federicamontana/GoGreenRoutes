import pandas as pd

df = pd.read_csv('df2.csv')
df_park = df[df['text1'].str.contains('shannon')]
#df_park['liststring'] = df_park['hashtag'].apply(lambda x: x[1:-1])
words = df_park['hashtag'].head(100).sum()
l = []
for x in words:
    if x not in l:
        l.append(x)





df_result = df_park.explode("liststring").groupby(by="liststring")["result"].count().sort_values(ascending=False)
df_result.reset_index(name="count")

results = []

for word in x.split():
    if word == value:
        results.append(word)
   