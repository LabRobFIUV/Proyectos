import numpy as np
import cv2
import time
import os 

class GetData():
	def __init__(self,name='video.avi'):
		self.name=name
		self.points=[]
		self.prom=0
		self.video=0
		self.show=False

	def Analyze(self):
		self.video=cv2.VideoWriter('s'+self.name,cv2.cv.CV_FOURCC('M','J','P','G'),20,(320,240),True)
		bytes,cresta = '',[]
		lower_c = np.array((137,86,0))
		upper_c = np.array((180,216,99))

		cap = cv2.VideoCapture(self.name)
		p,frame = cap.read()
		while p:
			hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			thresh = cv2.inRange(hsv,lower_c,upper_c)
			thresh = cv2.medianBlur(thresh,7)
			thresh2 = thresh.copy()
			countours, _ = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
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
				print "Fuera del Area"
			coord = cx, cy

			cv2.line(frame,(0,120),(340,120),(0,255,0),1)  # LINEA VERDE DEL CENTRO
			if not (coord in self.points):
				if (cx != 0):
					self.points.append(coord)
			w = len(self.points)

			for i in range(0,w-1):
				if self.points[i][0]<100:
					cv2.line(frame, (self.points[i]),(self.points[i+1]),(255,0,0),1) # LINEA AZUL DE LA ONDA
				elif self.points[i][0]<200:
					cv2.line(frame, (self.points[i]),(self.points[i+1]),(0,0,255),1) # LINEA AZUL DE LA ONDA
				else:
					cv2.line(frame, (self.points[i]),(self.points[i+1]),(0,255,0),1) # LINEA AZUL DE LA ONDA
				self.prom = self.points[i][1] + self.prom
			self.prom = self.prom / w

			cv2.line(frame, (self.points[0][0],self.prom), (self.points[w-1][0],self.prom),(255,255,255),1) #LINEA PROMEDIO
			cv2.line(frame,(self.points[0]),(self.points[w-1]),(255,255,255),1)  # LINEA BLANCA QUE SIGUE AL NAO DEL INICIO AL CENTRO Y FORMA LAS CURVAS

			crest = []
			for i in range (10,w-5):
				if not (self.points[i] in crest):
					if (self.points[i-3][1] > self.points[i][1]) and (self.points[i+3][1] > self.points[i][1]):
						crest.append(self.points[i])

			o = len(crest)
			if (o > 2):
				for i in range(0,o-1):
					cv2.line(frame,crest[i],crest[i+1],(255,148,148),1)  # LINEA DE PUNTO-PUNTO CRESTAS
			try:
				self.video.write(frame)
			except:
				print"Hubo algun error"

			if self.show:
				cv2.imshow('Camara',frame)
				cv2.imshow('Objeto',thresh2)
				if cv2.waitKey(1) == 1048603:
					print "Exit"

			p,frame = cap.read()

		f = open('posiciones.txt','wa')
		print "Streaming terminado"
		for i in range(0,len(self.points)-1):
			f.write(str(self.points[i][0]) + " " + str(self.points[i][1]) + "\n")

		dif = self.points[0][0] - self.prom
		if (dif < 0):
			dif = (dif * -1)

		res = dif *(1.90909090909090909090)
		int (res)
		f = open('distancia.txt','wa')
		f.write( "Diferencia en pixeles: " + str(dif) + "\n"
				+ "Diferencia en cm: " + str(res))
		f.close()
		self.video.release()
		os.remove(self.name)