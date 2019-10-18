from imutils.video import VideoStream
import threading
import time
import cv2

outputFrame = None
lock = threading.Lock()

def gen():
    global outputFrame
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    while True:
        frame = vs.read()
        with lock:
            outputFrame = frame.copy()
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

