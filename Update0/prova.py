import pandas as pd
import os 
import matplotlib.pyplot as plt
import seaborn as sns
from Read_dictionary_03 import emotions_liwc as emotions
os.chdir(r'/Users/FEDERICA/Desktop/GoGreenRoutes/Update0')
path_plot = os.path.abspath('plots')
df0 = pd.read_csv('df_prova.csv', index_col=[0])
park_list = ['ballyhoura','castletroy','shannon','arthur']

#mi prende il df del parco che mi interessa e mi calcola la statistica 
def df_byparks(park,df,emotions):
    df_park = df[df['text1'].str.contains(park)] #cerco i tweet che hanno quel parco all'interno del testo
    ds = df_park[emotions].describe()
    #df_park_media= pd.DataFrame({park: media}, index = emotions)
    return df_park, ds

#c'è un modo per farmi tornare diversi parchi in una volta?
df_ball, ds = df_byparks(park_list[0],df0,emotions)

def parks_mean(park_list,emotions):
    df_media_parks = pd.DataFrame()
    for park in park_list:
        df, ds = df_byparks(park,df0,emotions)
        media = ds.loc['mean'].to_list()
        df_m= pd.DataFrame({park: media}, index = emotions)
        df_media_parks = pd.concat([df_media_parks, df_m], axis =1)
    return df_media_parks


# def parks_mean(park_list,emotions):
#     df_media_parks = pd.DataFrame()
#     df_ball, ds_ball = df_byparks(park_list[0],df0,emotions)
#     df_cast, ds_cast = df_byparks(park_list[1],df0,emotions)
#     df_shan, ds_shan = df_byparks(park_list[2],df0,emotions)
#     df_art, ds_art = df_byparks(park_list[3],df0,emotions)
#     for park in park_list:
#         df, ds = df_byparks(park,df0,emotions)
#         media = ds.loc['mean'].to_list()
#         df_m= pd.DataFrame({park: media}, index = emotions)
#         df_media_parks = pd.concat([df_media_parks, df_m], axis =1)
#     return df_media_parks,df_ball, ds_ball,df_cast, ds_cast, df_shan, ds_shan,df_art, ds_art
def find_values(x,sent_list):
    results = []
    for value in sent_list:
        for word in x.split():
            if word == value:
                results.append(word)
    return results

df_park, ds = df_byparks('shannon',df0,emotions)
def explode(df,sent_list):
    #inserisco nella colonna result le parole dei tweet che si trovano nella lista
    df['result'] = df['text1'].apply(lambda x: find_values(x,sent_list))
    #elimino le righe in cui la colonna è vuota (perchè non ha trovato niente)
    df_match_list = df[df['result'].map(lambda d: len(d)) > 0]
    df_result = df_match_list.explode("result").groupby(by="result")["result"].count().sort_values(ascending=False)
    return df_result, df_match_list

#Pie chart of verage sentiment in a park (Ballyouhura)
def mean_pie(ds,save_name):
    plt.pie(ds.loc['mean'].to_list(), labels = emotions)
    sns.set(rc={'figure.figsize':(20,10)})
    plt.show()
    plt.savefig(os.path.join(path_plot,save_name))

mean_pie(ds,'prova.png')