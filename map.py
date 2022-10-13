
import folium
import base64
from folium import IFrame

# Create the map
m = folium.Map(location=[52.665920679645915, -8.625609956487203])
#Add Marker
encoded1 = base64.b64encode(open('C:\\Users\\micci\\Desktop\\GoGreenRoutes\\plots\\posneg\\shannon.png', "rb").read())
encoded2 = base64.b64encode(open('C:\\Users\\micci\\Desktop\\GoGreenRoutes\\plots\\posneg\\ballyhoura.png', "rb").read())
encoded3 = base64.b64encode(open('C:\\Users\\micci\\Desktop\\GoGreenRoutes\\plots\\posneg\\westfields.png', "rb").read())

html = '<img src="data:image/png;base64,{}">'.format
iframe1 = IFrame(html(encoded.decode('UTF-8')), width=400, height=350)
popup1 = folium.Popup(iframe, max_width=400)
iframe2 = IFrame(html(encoded.decode('UTF-8')), width=400, height=350)
popup2 = folium.Popup(iframe, max_width=400)
iframe3 = IFrame(html(encoded.decode('UTF-8')), width=400, height=350)
popup3 = folium.Popup(iframe, max_width=400)

folium.Marker(location=[52.660499089256234, -8.647512795443134], tooltip=html, popup = popup1, 
icon=folium.Icon(color = 'green')).add_to(m) #shannon
folium.Marker(location=[52.310711, -8.509693], tooltip=html, popup = popup2, 
icon=folium.Icon(color = 'green')).add_to(m) #ballyhoura
folium.Marker(location=[52.66216168516888, -8.646343871839647], tooltip=html, popup = popup3, 
icon=folium.Icon(color = 'green')).add_to(m) #westfield




