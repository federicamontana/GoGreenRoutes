import folium
import base64
from folium import IFrame

m = folium.Map(location=[52.6638, -8.6267])
m.save("plots/limerick_map.html")

tooltip = "Click me!"
 #Add Marker
encoded1 = base64.b64encode(open('plots/bar_chart/positive_shannon.png', 'rb').read())
encoded2 = base64.b64encode(open('plots/bar_chart/negative_shannon.png', 'rb').read())
html1 = '<img src="data:image/png;base64,{}">'.format
html2 = '<img src="data:image/png;base64,{}">'.format
iframe1 = IFrame(html1(encoded1.decode('UTF-8')), width=400, height=350)
iframe2 = IFrame(html2(encoded2.decode('UTF-8')), width=400, height=350)
popup = folium.Popup(iframe1,iframe2, max_width=400)

folium.Marker(location=[52.310711, -8.509693], tooltip=html, popup = popup, 
icon=folium.Icon(color = 'gray')).add_to(m)

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







