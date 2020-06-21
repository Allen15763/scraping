#7-11
# data request
import requests

#進行 POST 請求時要攜帶資料
form_data = {
    "commandid": "GetTown",
    "cityid": "01"
}
request_url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
response = requests.post(request_url, data=form_data)
print(response.status_code)  #200
response_content = response.content
print(type(response_content))  # class bytes
print(response_content)



#district selection
from lxml import etree  #decipher ElementTree
from io import BytesIO

file = BytesIO(response_content)
tree = etree.parse(file)  #tree type=lxml.etree._ElementTree
town_names = [t.text for t in tree.xpath("//TownName")] # XPath 亦可以指定 /iMapSDKOutput/GeoPosition/TownName
print(town_names)


form_data = {
    "commandid": "SearchStore",
    "city": "台北市",
    "town": "松山區",
}
request_url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
response = requests.post(request_url, data=form_data)
response_content = response.content
file = BytesIO(response_content)
tree = etree.parse(file)  #tree type=lxml.etree._ElementTree
poinames = [e.text for e in tree.xpath("//POIName")]
print(poinames)


#all store info
import time
import random

tp_711_stores = {}
for town in town_names:
    form_data = {
        "commandid": "SearchStore",
        "city": "台北市",
        "town": town
    }
    r = requests.post("https://emap.pcsc.com.tw/EMapSDK.aspx", data=form_data)
    f = BytesIO(r.content)
    tree = etree.parse(f)
    poi_ids = [t.text.strip() for t in tree.xpath("//POIID")]
    poi_names = [t.text for t in tree.xpath("//POIName")]
    lons = [float(t.text)/1000000 for t in tree.xpath("//X")]
    lats = [float(t.text)/1000000 for t in tree.xpath("//Y")]
    adds = [t.text for t in tree.xpath("//Address")]
    tp_711_stores[town] = []
    for poi_id, poi_name, lon, lat, add in zip(poi_ids, poi_names, lons, lats, adds):
        store_info = {
            "POIID": poi_id,
            "POIName": poi_name,
            "Longitude": lon,
            "Latitude": lat,
            "Address": add
        }
        tp_711_stores[town].append(store_info)
    time.sleep(random.randint(1, 6))
    print("Scraping {}".format(town))

print(tp_711_stores["松山區"][0])
print(tp_711_stores["信義區"][0])
print(tp_711_stores["大安區"][0])