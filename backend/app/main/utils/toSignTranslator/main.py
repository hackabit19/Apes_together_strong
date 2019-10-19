import speech_recognition as sr
import numpy as np
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
import os
import requests
#import selecting
# obtain audio from the microphone
dir_path = os.path.dirname(os.path.realpath(__file__))

def func(url_to_audio=None):

    if url_to_audio is not None:
        r = requests.get(url_to_audio, allow_redirects=True, stream=True)
        with open(os.path.join(dir_path, 'test.wav'), 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)

    r = sr.Recognizer()
    isl_gif=['all the best', 'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
            'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
            'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
            'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
            'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
             'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
            'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
            'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call an ambulance', 'please call me later',
            'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
            'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
            'what are you doing', 'what is the problem', 'what is todays date', 'what is your age', 'what is your father do', 'what is your job',
            'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
            'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
'bihar','bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile','dasara',
'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
'voice', 'wednesday', 'weight']


    arr=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
    's','t','u','v','w','x','y','z']
    with sr.AudioFile(os.path.join(dir_path, 'test.wav')) as source:
        r.adjust_for_ambient_noise(source)
        i=0
        r.pause_threshold = 3
        audio = r.listen(source)

        # recognize speech using Sphinx
        a=r.recognize_google(audio)
        print("you said " + a.lower())

        for c in string.punctuation:
            a= a.replace(c,"")

        if a.lower() in isl_gif:
            print(os.path.join(dir_path, 'ISL_Gifs/{0}.gif'.format(a.lower())))
            return os.path.join(dir_path, 'ISL_Gifs/{0}.gif'.format(a.lower()))
        else:
            images = []
            for i in range(len(a)):
                if a[i] in arr:
                    ImageAddress = os.path.join(dir_path, 'letters/'+a[i]+'.jpg')
                    images.append(ImageAddress)
                    # ImageItself = Image.open(ImageAddress)
                    # ImageNumpyFormat = np.asarray(ImageItself)
                    # plt.imshow(ImageNumpyFormat)
                    # plt.draw()
                    # plt.pause(0.8) # pause how many seconds
                    #plt.close()
                else:
                    continue
            video_name = 'output.avi'
            frame = cv2.imread(images[0])
            height, width, layers = frame.shape

            video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

            for image in images:
                for _ in range(20):
                    video.write(cv2.imread(image))

            cv2.destroyAllWindows()
            video.release()
            print(os.path.join(dir_path, 'output.avi'))
            return os.path.join(dir_path, 'output.avi')

# func()
