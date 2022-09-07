#Compute the mean of the sentiment in a certain park 
def aggregation(sent,df_s,aggr,labels):
    num = '{0:.3f}'.format(df_s[sent].mean()) #mean
    print(sent, ": ",  num ) 
    num = float(num)
    return aggr.append(num), labels.append(sent)


# def create_df():
#     data = {'data': data,
#            'labels': labels}
#     df = pd.DataFrame(data)
#     return df
