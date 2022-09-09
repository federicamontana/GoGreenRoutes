import pandas as pd

label = ['fear',
 'anger',
 'trust',
 'surprise',
 'positive',
 'negative',
 'sadness',
 'disgust',
 'joy',
 'anticipation']

#Compute the mean of the sentiment in a certain park 
def aggregation(sent,df_s,aggr,labels):
    num = '{0:.3f}'.format(df_s[sent].mean()) #mean
    print(sent, ": ",  num ) 
    num = float(num)
    return aggr.append(num), labels.append(sent)


def count_words(sent,df,result_dn):
    dn= pd.Series(df.apply(lambda i: i.astype(str).str.contains(sent).any(), axis=0),name='bool').to_frame().reset_index()
    result_dn[sent] = dn.loc[dn['bool']==True].drop('bool', axis=1)
    d = result_dn.to_dict(orient='list')
    # mask = pd.Series(df.apply(lambda i: i.astype(str).str.contains(sent).any(), axis=0), name='bool')
    # df2 = pd.DataFrame({sent:mask.index, 'bool':mask.values})
    # result_dn[sent]= df2.loc[df2['bool']==True].drop('bool', axis=1)
    return d

def new_df(sent,df,df2):
    df2[sent] = df.apply(lambda i: i.astype(str).str.contains(sent).any(), axis=0).astype(int)
    return df2
   
