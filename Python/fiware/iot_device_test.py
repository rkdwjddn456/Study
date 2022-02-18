import requests
import json
import time
from multiprocessing import Process

def controlLamp():
    Flag = False
    onOff = 'off'
    openClose = 'lock'

    while True:
        if Flag:
            onOff = 'on'
            openClose = 'unlock'
            Flag = False
        else:
            onOff = 'off'
            openClose = 'lock'
            Flag = True

        url = 'http://localhost:1026/v2/entities/urn:ngsi-ld:Lamp:001/attrs'
        headers = {'Content-Type':'application/json', 'fiware-service':'openiot', 'fiware-servicepath':'/'}
        data = {
            onOff : {
                'type' : 'command',
                'value' : ''
            }
        }

        response = requests.patch(url, headers=headers, data=json.dumps(data))
        response.close()

        time.sleep(0.5)

        url = 'http://localhost:1026/v2/entities/urn:ngsi-ld:Door:001/attrs'
        headers = {'Content-Type': 'application/json', 'fiware-service': 'openiot', 'fiware-servicepath': '/'}
        data = {
            openClose: {
                'type': 'command',
                'value': ''
            }
        }

        response = requests.patch(url, headers=headers, data=json.dumps(data))
        response.close()

        time.sleep(0.5)

if __name__ == "__main__":
    controlLamp()
#파이썬 IoT Device Request