import numpy as np
import cv2
import time
import requests
import threading
import urllib
from threading import Thread, Event, ThreadError

hue = 10
sat = 10
val = 10
hue2 = 180
sat2 = 255	
val2 = 255


  def __init__(self, url):
    
    self.stream = requests.get(url, stream=True)
    self.thread_cancelled = False
    self.thread = Thread(target=self.run)
    print "camera initialised"

  def nothing():
    pass

  def start(self):
    self.thread.start()
    print "camera stream started"
    
  def run(self):
    bytes=''
    points = []
    global hue
    global sat
    global val
    while not self.thread_cancelled:
      try:
        bytes+=self.stream.raw.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
          jpg = bytes[a:b+2]
          bytes= bytes[b+2:]

          img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

          frame = cv2.blur(img,(3,3))

          h = cv2.getTrackbarPos('H','Objeto')
          s = cv2.getTrackbarPos('S','Objeto')
          v = cv2.getTrackbarPos('V','Objeto')
          h2 = cv2.getTrackbarPos('H','Camera')
          s2 = cv2.getTrackbarPos('S','Camera')
          v2 = cv2.getTrackbarPos('V','Camera')

          lower = np.array([h,s,v])
          upper = np.array([h2,s2,v2])

          hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
          hsv2 = hsv.copy()
          thresh = cv2.inRange(hsv,lower, upper)
          thresh = cv2.medianBlur(thresh,7)
          thresh2 = thresh.copy()

          contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

          max_area = 0
          best_cnt = 1
          area = 0

          for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
              max_area = area
              best_cnt = cnt

          M = cv2.moments(best_cnt)
          cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
          #print cx,cy
          coord = cx,cy

          cv2.line(frame,(0,120),(340,120),(0,255,0),1)

          if not (coord in points):
          	if (cx != 0):
          		print "Ya esta"
          		points.append(coord)

          w = len(points)

          for i in range(0,w-1):
            cv2.line(frame,(points[i]),(points[i+1]),(255,0,0),1)
            prom = points[i][1] + prom

          prom = prom / w
          int(prom)


          for i in range(0,w-1):
          	cv2.line(frame,(points[i][0],prom),(points[i+1][0],prom),(255,255,0),1)
          	
          cv2.line(frame,(points[0]),(points[w-1]),(255,255,255),1)

          try:
            video.write(frame)
          except:    
            print "En algo te equivocaste noob"

          
          cv2.imshow('Camera',frame)
          cv2.imshow('Objeto',thresh2)

          #cv2.createTrackbar('valor H', 'Rojo', hue, 180, change_hue)
          #cv2.createTrackbar('valor S', 'Rojo', sat, 255, change_saturation)
          #cv2.createTrackbar('valor V', 'Rojo', val, 255, change_value)

          if cv2.waitKey(1) ==1048603:
          	f = open('posiciones.txt','wa')
          	for i in range(0,w):
          		f.write(str(points[i])+"\n")
          	print points[0][0]
          	exit(0)
          	f.close()
          	video.release()

          

      except ThreadError:
        self.thread_cancelled = True

  cv2.namedWindow('Camera',cv2.CV_WINDOW_AUTOSIZE)
  cv2.namedWindow('Rojo',cv2.CV_WINDOW_AUTOSIZE)
  cv2.createTrackbar('H', 'Rojo', hue, 180, nothing)
  cv2.createTrackbar('S', 'Rojo', sat, 255, nothing)
  cv2.createTrackbar('V', 'Rojo', val, 255, nothing)
  cv2.createTrackbar('H', 'Camera', hue2, 180, nothing)
  cv2.createTrackbar('S', 'Camera', sat2, 255, nothing)
  cv2.createTrackbar('V', 'Camera', val2, 255, nothing)
        
        
  def is_running(self):
    return self.thread.isAlive()
      
    
  def shut_down(self):
    self.thread_cancelled = True
    #block while waiting for thread to terminate
    while self.thread.isAlive():
      time.sleep(1)
    return True

  #posiciona la camara hacia el piso
  def move_camera(self):
    abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"

    for x in range(0,3):
      content = urllib.urlopen(abajo).read()


  
    
if __name__ == "__main__":
  url = 'http://192.168.0.100/image'
  cam = Cam(url)
  cam.move_camera()
  cam.start()
