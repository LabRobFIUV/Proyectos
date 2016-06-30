import numpy as np
import cv2
import time
import requests
import threading
import urllib
from threading import Thread, Event, ThreadError

class Tobject():
	def __init__(self,url):
		self.stream = requests.get(url, stream = True)
		self.thread_cancelled = False
		self.thread = Thread(target = self.Play)
		cv2.namedWindow('Camara',cv2.CV_WINDOW_AUTOSIZE)
		cv2.namedWindow('Objeto',cv2.CV_WINDOW_AUTOSIZE)

	def start(self):
		self.thread.start()

	def Play(self):
		points = []
		bytes,cresta,fps = '',[],20
		capSize =(320,240)
		codec = cv2.cv.CV_FOURCC('M','J','P','G')
		self.video = cv2.VideoWriter('video.avi',codec,fps,capSize,True)

		self.videoC = cv2.VideoWriter('videoT.avi',codec,fps,capSize,True)
		lower_c = np.array((137,86,0))
		upper_c = np.array((180,216,99))

		val = 0
		while not self.thread_cancelled:
			try:
				bytes+= self.stream.raw.read(1024)
				a = bytes.find('\xff\xd8')
				b = bytes.find('\xff\xd9')

				if a!=-1 and b!=-1:
					jpg = bytes[a:b+2]
					bytes = bytes[b+2:]
					img =  cv2.imdecode(np.fromstring(jpg, dtype = np.uint8),cv2.IMREAD_COLOR)
					frame = cv2.blur(img,(3,3))

					hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
					thresh = cv2.inRange(hsv,lower_c,upper_c)
					thresh = cv2.medianBlur(thresh,7)
					thresh2 = thresh.copy()
					countours, _ = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
					val = val + 1
					max_area,best_cnt,area = 0,0,0

					for cnt in countours:
						area = cv2.contourArea(cnt)
						if area > max_area:
							max_area = area
							best_cnt = cnt
					M = cv2.moments(best_cnt)

					cx,cy=0,0
					try:
						cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
					except:
						self.thread_cancelled =  True
						self.video.release()
#					cv2.line(frame,(0,120),(340,120),(0,255,0),1)  # LINEA VERDE DEL CENTRO

					try:
						self.videoC.write(frame)
					except:
						print"Hubo algun error"

					if 200>cx>100:
						try:
							if self.posIni==0:
								self.posIni = val -1
							band=True
							self.video.write(frame)
						except:
							print"Hubo algun error"
					if cx>=200 and self.posFin==0:
						self.posFin = val -1

					cv2.imshow('Camara',frame)
					cv2.imshow('Objeto',thresh2)

					if cv2.waitKey(1) == 1048603:
						self.thread_cancelled = True
						self.video.release()
						self.videoC.release()
			except ThreadError:
				self.thread_cancelled = True

	def end_cam(self):
		self.thread_cancelled = True

	def is_running(self):
		return self.thread.isAlive()

	def shut_down(self):
		self.thread_cancelled =  True
		while self.thread.isAlive():
			time.sleep(1)
		return True

	def move_camera(self):
		abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"

		for i in range(0,3):
			content = urllib.urlopen(abajo).read()