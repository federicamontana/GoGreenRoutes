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


from PIL import Image
#Read the two images
image1 = Image.open('plots/bar_chart/positive_shannon.png')
image1.show()
image2 = Image.open('plots/bar_chart/negative_shannon.png')
image2.show()
image1_size = image1.size
image2_size = image2.size
new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
new_image.paste(image1,(0,0))
new_image.paste(image2,(image1_size[0],0))
new_image.save("plots/merged_image.png")
new_image.show()

