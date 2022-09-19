from Sentiment_lists import fear_list, anger_list, trust_list, surprise_list, positive_list, negative_list, sadness_list, disgust_list, joy_list, anticipation_list
import numpy as np

# function to get intersection values
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
# function to get unique values
def unique(list1):
    x = np.array(list1)
    return np.unique(x)


l1 = anticipation_list
l2 = joy_list
lst_common = intersection(l1,l2)
print("Intersezione :",len(lst_common))

auxiliaryList = []
for word in l1:
    if word not in lst_common:
        auxiliaryList.append(word)
print("Unique words :",len(auxiliaryList))

  

  
  


