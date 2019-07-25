from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
import time
import cv2
sz = (320, 240)
def initCamera():
    camera = PiCamera()
    camera.resolution = sz
    camera.framerate = 32
    camera.iso = 800
    camera.brightness = 70
    rawCapture = PiRGBArray(camera, size=sz)
    time.sleep(0.1)
    return rawCapture,camera

rawCapture,camera=initCamera()
while 1:
    rawCapture = PiRGBArray(camera, size=sz)
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('192.168.1.109',10010))
    server.listen(5)
    print("waiting")
    connect,addr=server.accept()
    print("{} connected".format(addr))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        #ret, imgencode = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 50])
        ret, imgencode = cv2.imencode('.jpg', image)
        try:
            connect.sendall(imgencode)
        except:
            print("connection failed!!!")
            break
        #print("Received:{}\r".format(data))
        rawCapture.truncate(0)
    server.close()

