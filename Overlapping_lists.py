from Sentiment_lists import fear_list, anger_list, trust_list, surprise_list, positive_list, negative_list, sadness_list, disgust_list, joy_list, anticipation_list

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
l2 = joy_list
#JOY, SURPRISE, TRUST, ANTICIPATION
lst_common = intersection(positive_list, l2)
print(len(positive_list))
print(len(l2))
print(len(lst_common))



#L'intersezione tra joy,surp,trust,anticip e positive ci dice che
#tutte le parole che hanno joy,surp,ecc hanno anche positive
#Stessa cosa per negative
#len(negative_list)  = 3322

# len(joy_list)+len(surprise_list)+len(trust_list)
# +len(anticipation_list) = 3183
# len(positive_list) = 2303
#Tra i sottogruppi ci sono parole in comune

#JOY,SURPRISE
lst_common_joy_surp = intersection(surprise_list, joy_list) #176 parole in comunue
lst_common_joy_trust = intersection(trust_list, joy_list) #359 parole in comunue
lst_common_joy_ant = intersection(anticipation_list, joy_list) #362 parole in comunue

lst_common_surp_trust = intersection(trust_list, surprise_list) #106 parole in comunue
lst_common_surp_ant = intersection(anticipation_list, surprise_list) #186 parole in comunue

lst_common_trust_ant = intersection(anticipation_list, trust_list) #281 parole in comunue


if sorted(lst_int) == sorted(lst_common):
    print ("The lists are identical")
else :
    print ("The lists are not identical")