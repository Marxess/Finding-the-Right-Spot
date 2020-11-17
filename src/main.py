import * from funciones.py
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import os
import requests
import json
from dotenv import load_dotenv
from pymongo import MongoClient
import geopandas as gpd
from functools import reduce
import operator
import geopandas as gpd

#checking connection and getting the database 'companies'
conn = MongoClient("localhost:27017")
db = conn.get_database("ironhack")
collection = db.get_collection("companies")

c = collection

pd.DataFrame(c.find(
    {"$and": [
        {"offices.city": 'Dublin'},
        {"total_money_raised": {'$gt': '1.0'}}
    ]},
    {"name": 1, "rating": 1, "total_money_raised": 1, 'offices.latitude':1, 'offices.longitude':1}
))

dublin = {'type': 'Point', 'coordinates': [-6.25415, 53.32306]}
clavis_tech = {'type': 'Point', 'coordinates': [-6.258292, 53.346976]}

#map_dublin
map_dublin = folium.Map(location = [53.346976,-6.258292], zoom_start = 15)

#Adding Clavis Technologies (searched coordinates in google maps since the data was missing from companies' database)
#Location Clavis
clavis_lat =  53.346976
clavis_long = -6.258292

#creating the icon for Clavis
icono = Icon(color = "red",
             prefix = "fa",
             icon = "briefcase",
             icon_color = "black",
             tooltip = "Clavis Tech"
)
loc = [clavis_lat, clavis_long]
#saving the marker in one variable
marker_clavis = Marker(location = loc, icon = icono)
#let's add the marker to the original dublin map where we already had Dial2do location saved
marker_clavis.add_to(map_dublin)
map_dublin

#Starbucks 
load_dotenv()
tok1 = os.getenv("tok1")
tok2 = os.getenv("tok2")
#url and Starbucks venue chain ID
enlace = 'https://api.foursquare.com/v2/venues/explore'
starbucks = "556f676fbd6a75a99038d8ec"
#params to be taken into account in calling FourSquare API
parametros = { "client_id" : tok1,
          "client_secret" : tok2,
          "v" : "20180323",
          "ll": f"{clavis_tech.get('coordinates')[1]},{clavis_tech.get('coordinates')[0]}",
          "query": "starbucks",
          "limit" : 10
}
resp = requests.get (url = enlace, params = parametros)
data = json.loads(resp.text)
decoding_data = data.get('response')
decoded = decoding_data.get('groups')[0]
starbucks = decoded.get('items')
mapa_nombre = ["venue","name"]
latitud = ["venue", "location","lat"]
longitud = ["venue","location","lng"]
new_list = []
for diccionario in starbucks:
    starbuckslist = {}
    starbuckslist["name"] = getFromDict(diccionario,mapa_nombre)
    starbuckslist["latitud"] = getFromDict(diccionario,latitud)
    starbuckslist["longitud"] = getFromDict(diccionario,longitud)
    new_list.append(starbuckslist)
    dataframestarbucks = pd.DataFrame(new_list)
dataframestarbucks.head()

#Let's see which starbucks is closer to Clavis Tech
clavis_tech_coord = 53.346976,  -6.258292
starbucks = {
    'Starbucks_0': (53.347591,  -6.259555),
    'Starbucks_1': (53.350007,  -6.259033),
    'Starbucks_2': (53.349626, -6.261584),
    'Starbucks_3': (53.347545,  -6.263520),
    'Starbucks_4': (53.346098,  -6.259072)
}

for places, coord in starbucks.items():
    distance = haversine(clavis_tech_coord, coord)
    print(places, distance)
#We can see the closest Starbucks is c.100m away -> chosen starbucks

#Adding closest Starbucks to dublin map
#Location Clavis
starbucks_lat =  53.347591
starbucks_long = -6.259555

#creating the icon for Starbucks
icono = Icon(color = "darkgreen",
             prefix = "fa",
             icon = "coffee",
             icon_color = "black",
             tooltip = "Starbucks"
)
loc = [starbucks_lat, starbucks_long]
#saving the marker in one variable
marker_starbucks = Marker(location = loc, icon = icono)
#let's add the marker to the map where we already had Clavis Tech location saved
marker_starbucks.add_to(map_dublin)
map_dublin


#Irish Pubs
enlace = 'https://api.foursquare.com/v2/venues/explore'
irish_pubs = "52e81612bcbc57f1066b7a06"
parametros = { "client_id" : tok1,
          "client_secret" : tok2,
          "v" : "20180323",
          "ll": f"{clavis_tech.get('coordinates')[1]},{clavis_tech.get('coordinates')[0]}",
          "query": "irish_pubs",
          "limit" : 10
}
resp = requests.get (url = enlace, params = parametros)
data = json.loads(resp.text)
decoding_data = data.get('response')
decoded = decoding_data.get('groups')[0]
irish_pubs = decoded.get('items')
mapa_nombre = ["venue","name"]
latitud = ["venue", "location","lat"]
longitud = ["venue","location","lng"]
new_list2 = []
for diccionario in irish_pubs:
    irishpubslist = {}
    irishpubslist["name"] = getFromDict(diccionario,mapa_nombre)
    irishpubslist["latitud"] = getFromDict(diccionario,latitud)
    irishpubslist["longitud"] = getFromDict(diccionario,longitud)
    new_list2.append(irishpubslist)
    
dataframeirish = pd.DataFrame(new_list2)
dataframeirish.head()

#Let's now calculate distantes to irish pubs
clavis_tech_coord = 53.346976,  -6.258292
irish_pubs = {
    'Irish Whiskey Museum': (53.344338,  -6.259548),
    'The Quays': (53.345554,  -6.263121),
    'Irish Rock ‘N’ Roll Museum Experience': (53.344976, -6.264444),
    'Irish Film Institute (IFI)': (53.344667,  -6.265295),
    'Irish Design Shop': (53.342667,  -6.263078)
}

for places, coord in irish_pubs.items():
    distance = haversine(clavis_tech_coord, coord)
    print(places, distance)
#We can see there are many irish pubs nearby: Irish Whiskey Museum and the Quays less than 400m away

#Adding closest Irish pub to dublin map
#Location Irish Pub
pub_lat =  53.344338
pub_long = -6.259548

#creating the icon for Irish Pub
icono = Icon(color = "orange",
             prefix = "fa",
             icon = "beer",
             icon_color = "black",
             tooltip = "Irish Pub"
)
loc = [pub_lat, pub_long]
#saving the marker in one variable
marker_pub = Marker(location = loc, icon = icono)
#let's add the marker to the map where we already had Clavis Tech location and other markers saved
marker_pub.add_to(map_dublin)
map_dublin

#Looking for dog vet service
enlace = 'https://api.foursquare.com/v2/venues/explore'
vet = "4d954af4a243a5684765b473"
parametros = { "client_id" : tok1,
          "client_secret" : tok2,
          "v" : "20180323",
          "ll": f"{clavis_tech.get('coordinates')[1]},{clavis_tech.get('coordinates')[0]}",
          "query": "vet",
          "limit" : 10
}

resp = requests.get (url = enlace, params = parametros)
data = json.loads(resp.text)
decoding_data = data.get('response')
decoded = decoding_data.get('groups')[0]
vet = decoded.get('items')

new_list3 = []
for diccionario in vet:
    vetlist = {}
    vetlist["name"] = getFromDict(diccionario,mapa_nombre)
    vetlist["latitud"] = getFromDict(diccionario,latitud)
    vetlist["longitud"] = getFromDict(diccionario,longitud)
    new_list3.append(vetlist)
    
dataframevet = pd.DataFrame(new_list3)
dataframevet.head()

#Let's now calculate distantes to dog vet services
clavis_tech_coord = 53.346976,  -6.258292
vet_serv = {
    'The Porterhouse': (53.345159,  -6.267517),
    'Duleek Vet Hospital': (53.655193,  -6.416615),
    'Vet Farm Supplies': (53.525459, -7.344558),
    'Shannon Vet Surgery': (53.423706,  -7.983576)
}

for places, coord in vet_serv.items():
    distance = haversine(clavis_tech_coord, coord)
    print(places, distance)
#We can see there is a veterinarian where we could find a hairdresser for the dog (650m away)

#Adding closest vet to dublin map
#Location Vet
vet_lat =  53.345159
vet_long = -6.267517

#creating the icon for Veterinarian
icono = Icon(color = "blue",
             prefix = "fa",
             icon = "paw",
             icon_color = "black",
             tooltip = "Veterinarian"
)
loc = [vet_lat, vet_long]
#saving the marker in one variable
marker_vet = Marker(location = loc, icon = icono)
#let's add the marker to the map where we the other locations and markers saved
marker_vet.add_to(map_dublin)
map_dublin


#Conclusion -> Clavis Tech office buildings seem to be the perfect spot for the new gaming company since it meets all the above mentioned requirements.The coordinates are: [-6.258292, 53.346976].