print(df['text1'].astype('string'))
# Since our data frame contains separate tweet strings, 
# we will join them to create a string object containing all of our tweets
str_tweet = ",".join(df["text1"])
str_tweet = str_tweet.split()

# Let's for ex calculate the frequencies
for i in range(len(str_tweet)):
    text_object = NRCLex(str_tweet[i])

# creation of the new dictionary
my_emolex = emolex_df[emolex_df["word"].isin(str_tweet)]

# How many words does each emotion have? 
em_count = my_emolex[my_emolex.association == 1].emotion.value_counts()

# Plot
labels = ["positive", "trust", "negative", "anticipation", "joy", "fear", "anger", "surprise", "sadness", "disgust"]
mycolors = ["AliceBlue", "Aquamarine", "Coral", "LightGreen", "LightSkyBlue", "Violet", "Teal", "Tomato", "PapayaWhip", "Khaki"]
plt.pie(em_count, labels = labels, colors = mycolors)