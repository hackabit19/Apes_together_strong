import os
import requests
import pdf2image
import PyPDF2
import wave
from PIL import Image
import urllib
import io
import time
import cv2
import operator
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
import json
from xml.etree import ElementTree

def pil_to_array(pil_image):
	image_byte_array = io.BytesIO()
	pil_image.save(image_byte_array, format='PNG')
	image_data = image_byte_array.getvalue()
	return image_data

_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/RecognizeText'
_key = "b6d6c5b4629a4cf18d3fe3949bd519c7"
  #Here you have to paste your primary key for vision
_maxNumRetries = 10

def processRequest( json, data, headers, params ):
	retries = 0
	result = None

	while True:
		response = requests.post(_url, json = json, data = data, headers = headers, params = params )

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
		response = requests.get(operationLocation, json=None, data=None, headers=headers, params=None)
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

def showResultinFile(result):
	lines = result['recognitionResult']['lines']
	texty = ""
	for i in range(len(lines)):
		words = lines[i]['words']
		s = ""
		for word in words:
			s += word['text'] + " "
		print(s)
		texty += s
	return texty

def text_from_image(image_data):
	params = {'mode' : 'Handwritten'}
	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'

	json = None

	operationLocation = processRequest(json, image_data, headers, params)
	print("Baahar")
	result = None
	if (operationLocation != None):
		headers = {}
		headers['Ocp-Apim-Subscription-Key'] = _key
		while True:
			time.sleep(1)
			print("Trying")
			result = getOCRTextResult(operationLocation, headers)
			print("Nikal Lawde")
			if result['status'] == 'Succeeded' or result['status'] == 'Failed':
				break
	text_file = []
	if result is not None and result['status'] == 'Succeeded':
		data8uint = np.fromstring(image_data, np.uint8)
		img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
		return showResultinFile(result)
	# 	# showResultOnImage(result, img)
	# 	all_text = result['recognitionResult']['lines']
	# 	for i in range(len(all_text)):
	# 		one_line = all_text[i]['words']
	# 		each_line_as_string = ""
	# 		for word in one_line:
	# 			each_line_as_string += word['text'] + " "
	# 		text_file.append(each_line_as_string)
	# return text_file

subscription_key = "c49df94e6fc84d3a93768d94524f0007"

all_audio = []
# Here you have to paste the key for azure speech api
class TextToSpeech(object):
	def __init__(self, to_be_spoken, subscription_key):
		self.subscription_key = subscription_key
		self.tts = to_be_spoken
		self.timestr = time.strftime("%Y%m%d-%H%M")
		self.access_token = None

	def get_token(self):
		fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
		headers = {
			'Ocp-Apim-Subscription-Key': self.subscription_key
		}
		response = requests.post(fetch_token_url, headers=headers)
		self.access_token = str(response.text)

	def save_audio(self):
		base_url = 'https://westus.tts.speech.microsoft.com/'
		path = 'cognitiveservices/v1'
		constructed_url = base_url + path
		headers = {
			'Authorization': 'Bearer ' + self.access_token,
			'Content-Type': 'application/ssml+xml',
			'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
			'User-Agent': 'YOUR_RESOURCE_NAME'
		}
		xml_body = ElementTree.Element('speak', version='1.0')
		xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
		voice = ElementTree.SubElement(xml_body, 'voice')
		voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
		voice.set('name', 'en-US-Guy24kRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
		voice.text = self.tts
		body = ElementTree.tostring(xml_body)

		response = requests.post(constructed_url, headers=headers, data=body)
		if response.status_code == 200:
			with open('sample-' + self.timestr + '.wav', 'wb') as audio:
				audio.write(response.content)
				all_audio.append('sample-' + self.timestr + '.wav')
				print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
		else:
			print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
			print("Reason: " + str(response.reason) + "\n")

	def get_voices_list(self):
		base_url = 'https://westus.tts.speech.microsoft.com/'
		path = 'cognitiveservices/voices/list'
		constructed_url = base_url + path
		headers = {
			'Authorization': 'Bearer ' + self.access_token,
		}
		response = requests.get(constructed_url, headers=headers)
		if response.status_code == 200:
			print("\nAvailable voices: \n" + response.text)
		else:
			print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

def narrate_book(url, sound=False):     #This function returns text from the book.
	filename = "pdfExample.pdf"
	r = requests.get(url, allow_redirects=True, stream=True)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content():
			f.write(chunk)

	images = pdf2image.convert_from_path(filename)
	print(len(images))
	all_text = ""
	for image in images:
		image_data = pil_to_array(image)
		new_page = text_from_image(image_data)
		all_text += new_page
		if sound:
			app = TextToSpeech(new_page, subscription_key)
			app.get_token()
			app.save_audio()
			return combine_all_audio()
	return all_text

def combine_all_audio():
	global all_audio
	dir_path = os.path.dirname(os.path.realpath(__file__))
	data = []
	outfile = os.path.join(dir_path, "narration.wav")
	for infile in all_audio:
		w = wave.open(infile, 'rb')
		data.append([w.getparams(), w.readframes(w.getnframes())])
		w.close()

	print('audio elements = '+str(len(data)))

	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])
	for data_ele in data:
		output.writeframes(data_ele[1])
	output.close()
	all_audio = []
	return outfile

if __name__ == "__main__":
	url = "https://arxiv.org/pdf/1601.07255.pdf"
	all_text = narrate_book(url)
	combine_all_audio()
