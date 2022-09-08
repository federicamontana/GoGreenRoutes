import pandas as pd

#Compute the mean of the sentiment in a certain park 
def aggregation(sent,df_s,aggr,labels):
    num = '{0:.3f}'.format(df_s[sent].mean()) #mean
    print(sent, ": ",  num ) 
    num = float(num)
    return aggr.append(num), labels.append(sent)


def count_words(sent,df,result_dn):
    dn= pd.Series(df.apply(lambda i: i.astype(str).str.contains('anticipation').any(), axis=0),name='bool').to_frame().reset_index()
    result_dn[sent] = dn.loc[dn['bool']==True].drop('bool', axis=1)
    return result_dn
