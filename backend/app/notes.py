import time 
import requests
import cv2
import operator
import numpy as np
import math
import wave
import json
from xml.etree import ElementTree

_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/RecognizeText'
_key = "90101da0eaa3442d8f2e21bb4106b5bf"
_maxNumRetries = 10
subscription_key = "c49df94e6fc84d3a93768d94524f0007"

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

def gimme_text_and_bounding_boxs(img_path):
    pathToFileInDisk = img_path
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
    return result

# return Array(Tuple(string_type, string_val))
def gimme_proper_text(text_bnd_boxs_result, column_len, row_len):
    lines = text_bnd_boxs_result['recognitionResult']['lines']
    my_str = []
    k = 0
    for i in range(len(lines)):
        line_str = ""
        words = lines[i]['words']
        prev_mag = 0
        this_head = False
        for j in range(len(words)):
            tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
            tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
            br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
            bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
            text = words[j]['text']
            print(tl)
            line_str += " " + text
            font_size = math.sqrt((tl[0] - bl[0]) * (tl[0] - bl[0]) + (tl[1] - bl[1]) * (tl[1] - bl[1]))
            font_size += math.sqrt((tr[0] - br[0]) * (tr[0] - br[0]) + (tr[1] - br[1]) * (tr[1] - br[1]))
            font_size = font_size / 2
            if k == 0 and j == 0 and tl[0] > 0.7 * row_len and tl[1] < 0.2 * column_len:
                this_head = False
                line_str = ""
                break
            if k == 0 and j == 0 and tl[0] > 0.3 * row_len:
                this_head = True
            if k == 0 and j == (len(words) -1) and tl[0] < 0.8 * row_len:
                this_head = True
                break
            if k != 0 and this_head != True and (text.strip() in [':', '>', '='] or (prev_mag > font_size and (font_size - prev_mag) / font_size > 0.2)):
                my_str.append(["subtitle", line_str])
                line_str = ""
            if this_head == False and font_size > prev_mag:
                prev_mag = font_size
        if this_head == True:
            if k == 0:
                my_str.append(["title", line_str])
                k = 1
            else:
                my_str.append(["subtitle", line_str])
        elif len(line_str) != 0:
            my_str.append(["normal", line_str.strip()])
    return my_str

def gimme_the_final_text(text_with_types):
    text_to_be_spoken = ""
    for text_block in text_with_types:
        if text_block[0] == "title":
            text_to_be_spoken += ". The title of the text is: "
            text_to_be_spoken += text_block[1] + ".\n "
        elif text_block[0] == "subtitle":
            text_to_be_spoken += ". The subtitle is"
            text_to_be_spoken += text_block[1] + ".\n "
        else:
            text_to_be_spoken += text_block[1]
    return text_to_be_spoken

def get_my_audio_token(subscription_key):
    fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    return str(response.text)

def save_audio(access_token, text_to_be_spoken):
    # all_audio = []
    base_url = 'https://westus.tts.speech.microsoft.com/'
    path = 'cognitiveservices/v1'
    constructed_url = base_url + path
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'YOUR_RESOURCE_NAME'
    }
    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    voice.set('name', 'en-US-Guy24kRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
    voice.text = text_to_be_spoken
    body = ElementTree.tostring(xml_body)
    response = requests.post(constructed_url, headers=headers, data=body)
    if response.status_code == 200:
        with open('sample' + '.wav', 'wb') as audio:
            audio.write(response.content)
            # all_audio.append('sample-' + self.timestr + '.wav')
            print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
    else:
        print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
        print("Reason: " + str(response.reason) + "\n")

if __name__ == "__main__":
    img_path = r"./2hand_.png"
    shp =  cv2.imread(img_path).shape
    column_len = shp[0]
    row_len = shp[1]
    text_bnd_boxs_result = gimme_text_and_bounding_boxs(img_path)
    text_with_types = gimme_proper_text(text_bnd_boxs_result, column_len, row_len)
    text_to_be_spoken = gimme_the_final_text(text_with_types)
    access_token = get_my_audio_token(subscription_key)
    save_audio(access_token, text_to_be_spoken)
