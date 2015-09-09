import numpy as np
import cv2
import time
import requests
import threading
import urllib
from threading import Thread, Event, ThreadError

class Cam():

	def __init__(self,url):
		self.stream = requests.get(url, stream = True)
		self.thread_cancelled = False
		self.thread = Thread(target = self.run)
		print "Camara inicializada"

	def nothing():
		pass

	def start(self):
		self.thread.start()
		print "Streaming encendido"

	def run(self):

		bytes = ''
		prom = 0
		points = []
		cresta = []
		fps = 20
		capSize =(320,240)
		codec = cv2.cv.CV_FOURCC('M','J','P','G')

		lower_blue = np.array([123,118,93])
		upper_blue = np.array([180,255,255])

		video = cv2.VideoWriter('video.avi',codec,fps,capSize,True)

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
					hsv2 = hsv.copy()
					thresh = cv2.inRange(hsv,lower_blue,upper_blue)
					thresh = cv2.medianBlur(thresh,7)
					thresh2 = thresh.copy()

					countours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

					max_area = 0
					best_cnt = 0
					area = 0

					for cnt in countours:
						area = cv2.contourArea(cnt)
						if area > max_area:
							max_area = area
							best_cnt = cnt

					M = cv2.moments(best_cnt)
					cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
					coord = cx, cy

					cv2.line(frame,(0,120),(340,120),(0,255,0),1)

					#guarda las coordenadas si no estan repetidas, si el objeto no se mueve se guarda la misma pocision varias veces
					#
					if not (coord in points):
						if (cx != 0):
							points.append(coord)

					w = len(points)

					#Dibuja la onda senoidal
					for i in range(0,w-1):
						cv2.line(frame, (points[i]),(points[i+1]),(255,0,0),1)
						prom = points[i][1] + prom

					prom = prom / w
					int (prom)

					#Dibuja la linea promedio
					for i in range (0,w-1):
						cv2.line(frame, (points[i][0],prom), (points[i+1][0],prom),(255,255,0),1)

					#Dibuja la ruta que siguio de la posicion inicial a la final
					cv2.line(frame,(points[0]),(points[w-1]),(255,255,255),1)

					for i in range (10,w-5):
						if not (points[i] in cresta):
							if (points[i-3][1] < points[i][1]) and (points[i+3][1] < points[i][1]):
								cresta.append(points[i])
	
					o = len(cresta)
					if (o > 2):
						for i in range(0,o-1):
							cv2.line(frame,cresta[i],cresta[i+1],(255,148,148),1)

					try:
						video.write(frame)
					except:
						print"Hubo algun error"

					cv2.imshow('Camara',frame)
					cv2.imshow('Objeto',thresh2)

					if cv2.waitKey(1) == 1048603:
						print cresta
						f = open('posiciones.txt','wa')
						print "Streaming terminado"
						for i in range(0,len(points)-1):
							f.write(str(points[i][0]) + " " + str(points[i][1]) + "\n")

						dif = points[0][0] - prom
						#print dif
						#print points
						if (dif < 0):
							dif = (dif * -1)

						res = dif *(1.90909090909090909090)
						int (res)
						#print res
						f = open('distancia.txt','wa')
						f.write( "Diferencia en pixeles: " + str(dif) + "\n"
								+ "Diferencia en cm: " + str(res))
						f.close()
						exit(0)
						video.release()
			
			except ThreadError:
				self.thread_cancelled = True


	cv2.namedWindow('Camara',cv2.CV_WINDOW_AUTOSIZE)
	cv2.namedWindow('Objeto',cv2.CV_WINDOW_AUTOSIZE)

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

if __name__ == '__main__':
	url = "http://192.168.0.100/image"
	cam = Cam(url)
	cam.move_camera()
	cam.start()