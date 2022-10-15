####grafici insieme
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
park= 'westfields'
filepath = 'df_plot/df_neg_'+park+'.csv'
df = pd.read_csv(filepath)
fig, axes = plt.subplots(1, 2, figsize=(10,10))
fig.suptitle('Most frequent words in '+park+' park')
title_plot = 'Negative words'
sns.barplot(ax=axes[0], y= 'result', x = 'count',data = df[0:10])
axes[0].set_title(title_plot)
filepath = 'df_plot/df_pos_'+park+'.csv'
df = pd.read_csv(filepath)
title_plot = 'Positive words '
sns.barplot(ax=axes[1], y= 'result', x = 'count', data = df[0:10])
axes[1].set_title(title_plot)
plt.savefig('plots/posneg/'+park+'.png')







