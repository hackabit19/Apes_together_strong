from gevent import monkey
monkey.patch_all()

import speech_recognition as sr
import uuid
from flask import Flask, render_template, session, request, url_for, current_app
import wave
import uuid
import os
from gtts import gTTS
from flask_socketio import SocketIO, emit, join_room

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
socketio = SocketIO(app)

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/login')
def login():
    return render_template('login.html')

@socketio.on('message', namespace='/chat')
def chat_message(message):
    print("message = ", message)
    emit('message', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})
  
@socketio.on('chat-to-aud', namespace='/chat')
def chat_to_aud(message):
    print(message)
    audio = gTTS(message)
    name = str(uuid.uuid1()) + ".wav"
    audio.save(os.path.join(dir_path, 'static', '_files', name))
    print("done")
    emit('add-wavefile', url_for('static',
                                 filename='_files/' + name), broadcast=True)
    # os.remove(os.path.join(dir_path, 'static', '_files', 'message.wav'))
    
@socketio.on('start-recording', namespace='/chat')
def start_recording(options):
    """Start recording audio from the client."""
    id = uuid.uuid4().hex  # server-side filename
    session['wavename'] = id + '.wav'
    wf = wave.open(os.path.join(dir_path, 'static', '_files', session['wavename']), 'wb')
    wf.setnchannels(options.get('numChannels', 1))
    wf.setsampwidth(options.get('bps', 16) // 8)
    wf.setframerate(options.get('fps', 44100))
    
    session['wavefile'] = wf


@socketio.on('write-audio', namespace='/chat')
def write_audio(data):
    """Write a chunk of audio from the client."""
    session['wavefile'].writeframes(data)


def getTextFromAudio(filepath):
    r = sr.Recognizer()
    filepath = filepath[1:]
    filepath = os.path.join(dir_path, filepath)
    print(filepath)
    with sr.AudioFile(filepath) as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 3
        audio = r.listen(source)

        # recognize speech using Sphinx
        a=r.recognize_google(audio)
        return a.lower()

@socketio.on('end-recording', namespace='/chat')
def end_recording():
    """Stop recording audio from the client."""
    emit('add-wavefile', url_for('static',
                                 filename='_files/' + session['wavename']))
    text = getTextFromAudio(
      url_for('static', filename='_files/' + session['wavename']))
    print(text)
    emit('message', {'data': { 'message': text, 'author': 'by IM4ALL' }}, broadcast=True)
    print('here')
    session['wavefile'].close()
    del session['wavefile']
    del session['wavename']

if __name__ == '__main__':
  socketio.run(app)
  
