import numpy as np
import cv2
import time
import requests
import threading
import urllib
from threading import Thread, Event, ThreadError

class Camera():
	def __init__(self,url,name='video.avi'):
		self.name=name
		self.stream = requests.get(url, stream = True)
		self.thread_cancelled = False
		self.thread = Thread(target = self.run)
		self.show=False
		self.save=False
		self.frame=''
		self.video = 0

	def start(self):
		self.thread.start()
		time.sleep(1)

	def run(self):
		bytes,fps = '',20
		capSize =(320,240)
		codec = cv2.cv.CV_FOURCC('M','J','P','G')
		if self.save:
			self.video=cv2.VideoWriter(self.name,cv2.cv.CV_FOURCC('M','J','P','G'),20,(320,240),True)

		while not self.thread_cancelled:
			try:
				bytes+= self.stream.raw.read(1024)
				a = bytes.find('\xff\xd8')
				b = bytes.find('\xff\xd9')

				if a!=-1 and b!=-1:
					jpg = bytes[a:b+2]
					bytes = bytes[b+2:]
					img =  cv2.imdecode(np.fromstring(jpg, dtype = np.uint8),cv2.IMREAD_COLOR)
					self.frame = cv2.blur(img,(3,3))

					if self.save:
						try:
							self.video.write(self.frame)
						except:
							print"Error con el frame, saltando..."

					if self.show==True:
						cv2.imshow('Camara',self.frame)

						if cv2.waitKey(1) == 1048603:
							self.thread_cancelled = True

			except ThreadError:
				self.thread_cancelled = True

	def end_cam(self):
		self.thread_cancelled = True
		self.end_save()

	def is_running(self):
		return self.thread.isAlive()

	def shut_down(self):
		self.thread_cancelled =  True
		while self.thread.isAlive():
			time.sleep(1)
		return True

	def end_save(self):
		self.save=False
		self.video.release()

	def move_camera(self):
		abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"

		for i in range(0,3):
			content = urllib.urlopen(abajo).read()