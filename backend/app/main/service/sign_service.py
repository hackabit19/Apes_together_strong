from imutils.video import VideoStream
import threading
from app.main.service.recognize import recognize
import time
import cv2

outputFrame = None
lock = threading.Lock()

def gen():
    global outputFrame
    cam = cv2.VideoCapture(1)
    if cam.read()[0] == False:
        cam = cv2.VideoCapture(0)
    # vs = VideoStream(src=0).start()
    vs = cam
    time.sleep(1.0)
    while True:
        # frame = vs.read()
        with lock:
            outputFrame = recognize(vs)
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

