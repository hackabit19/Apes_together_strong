import time 
import requests
import cv2
import operator
import numpy as np

_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/RecognizeText'
_key = "90101da0eaa3442d8f2e21bb4106b5bf"
_maxNumRetries = 10

def processRequest( json, data, headers, params ):
    retries = 0
    result = None
    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break
    return result

def getOCRTextResult( operationLocation, headers ):
    retries = 0
    result = None
    while True:
        response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break
    return result

pathToFileInDisk = r"./3_hand.jpg"

with open(pathToFileInDisk, 'rb') as f:
    data = f.read()

# Computer Vision parameters
params = {'mode' : 'Handwritten'}

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

json = None

operationLocation = processRequest(json, data, headers, params)

result = None
if (operationLocation != None):
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = _key
    while True:
        time.sleep(1)
        result = getOCRTextResult(operationLocation, headers)
        if result['status'] == 'Succeeded' or result['status'] == 'Failed':
            break

lines = result['recognitionResult']['lines']

for i in range(len(lines)):
    words = lines[i]['words']
    for j in range(len(words)):
        tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
        tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
        br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
        bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
        text = words[j]['text']
        print(text)
