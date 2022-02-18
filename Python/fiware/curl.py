import json
import requests

url = "http://192.168.79.129:1026/v2/entities"
data = {
    "id": "urn:ngsi-ld:Store:001",
    "type": "Store",
    "address": {
        "type": "PostalAddress",
        "value": {
            "streetAddress": "Bornholmer Straße 65",
            "addressRegion": "Berlin",
            "addressLocality": "Prenzlauer Berg",
            "postalCode": "10439"
        },
        "metadata": {
            "verified": {
                "value": True,
                "type": "Boolean"
            }
        }
    },
    "location": {
        "type": "geo:json",
        "value": {
             "type": "Point",
             "coordinates": [13.3986, 52.5547]
        }
    },
    "name": {
        "type": "Text",
        "value": "Bösebrücke Einkauf"
    }
}

jLoad = json.dumps(data)
head = {"Content-Type": "application/json"}
res1 = requests.post(url , data= jLoad, headers=head)
print(res1.status_code)