# Bibliotecas necesarias
import cv2
import time
import math
import urllib
import motion
import requests
import threading
import numpy as np
from naoqi import ALProxy
from threading import Thread, Event, ThreadError

# punto de la pantalla donde se hizo click
point = [0,0]

# Funcion que pone de pie al Nao
def Parar():
	motionProxy.stiffnessInterpolation("Body",1,1.0)
	postureProxy.goToPosture("StandInit",1)

# Funcion que pone al Nao en postura de descanso
def Sentar():
	postureProxy.goToPosture("Crouch",1)
	motionProxy.stiffnessInterpolation("Body",0,1.0)

# Funcion que pone al Nao a caminar indeterminadamente
def Caminar():
	motionProxy.setWalkTargetVelocity(0.6,0,0,0.1)

# Funcion que deteniene la caminata
def Deternerse():
	motionProxy.setWalkTargetVelocity(0,0,0,0)

# Funcion que establece la posicion donde se hizo click
def mousePosition(event,x,y,flags,param):
	global point
	if event == cv2.EVENT_LBUTTONDOWN:
		point = [x,y]

# Clase principal
class Cam():
	# Funcion default
	def nothing(self, x):
		pass

	def Main(self):
		vA, ant_vA = 0, 90000
		points = []
		cv2.namedWindow('Camera',0)
		cv2.resizeWindow("Camera", 1000,750);
		cv2.setMouseCallback('Camera',mousePosition)
		band = False
		Gband =False
		thresh_cp1 = 0
		thresh_cp2 = 0

		cap = cv2.VideoCapture(0)
		ret, img = cap.read()
		while(ret):
			frame = cv2.blur(img,(3,3))
			if point[0]!=0 and point[1]!=0:
				frame[point[1]-1:point[1]+1,point[0]-1:point[0]+1]=[0,0,255]
				hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
				# Frente (color)
				lower_c1 = np.array([103,52,74])
				upper_c1 = np.array([151,198,170])
				# Atras (color)
				lower_c2 = np.array([15,151,145])
				upper_c2 = np.array([47,255,255])

				# Aplica threshold
				thresh_c1 = cv2.inRange(hsv,lower_c1,upper_c1)
				thresh_c1 = cv2.medianBlur(thresh_c1,7)
				thresh_c2 = cv2.inRange(hsv,lower_c2,upper_c2)
				thresh_c2 = cv2.medianBlur(thresh_c2,7)

				# Reespalda y busca contornos
				thresh_cp1 = thresh_c1.copy()
				thresh_cp2 = thresh_c2.copy()
				countours_c1, _ = cv2.findContours(thresh_c1, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
				countours_c2, _ = cv2.findContours(thresh_c2, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

				# Busca el area de mayor contorno en ambos umbrales (Inicia)
				max_area_c1, max_area_c2 = 0 , 0
				best_cnt_c1, best_cnt_c2 = 0 , 0
				area = 0
				tc1=len(countours_c1)
				tc2=len(countours_c2)
				tcm = 0

				if tc1>tc2:
					tcm=tc1
				else:
					tcm=tc2
				for i in range(tcm):
					if i<tc1 and cv2.contourArea(countours_c1[i])>max_area_c1:
						max_area_c1 = cv2.contourArea(countours_c1[i])
						best_cnt_c1 = countours_c1[i]
					if i<tc2 and cv2.contourArea(countours_c2[i])>max_area_c2:
						max_area_c2 = cv2.contourArea(countours_c2[i])
						best_cnt_c2 = countours_c2[i]
				# Busca el area de mayor contorno en ambos umbrales (Termina)

				# Calcula los momentos y las posiciones centrales de cada umbral
				M = cv2.moments(best_cnt_c1)
				M2 = cv2.moments(best_cnt_c2)
				coord1 = []
				coord2 = []
				try:
					cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
					coord1.append(cx)
					coord1.append(cy)
					cx,cy = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])
					coord2.append(cx)
					coord2.append(cy)
				except:
					# Si hubo error, la posicion guardada sera [0,0]
					coord1.append(0)
					coord1.append(0)
					coord2.append(0)
					coord2.append(0)

				# OBTERNER DISTANCIAS punto - frente - atras
				m01=((coord1[0]-point[0])**2+(coord1[1]-point[1])**2)
				m01=math.sqrt(m01)
				m02=((coord2[0]-point[0])**2+(coord2[1]-point[1])**2)
				m02=math.sqrt(m02)
				mxy=((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2)
				mxy=math.sqrt(mxy)

				if m01 != 0 and mxy != 0:
					vA=((m01)**2+(mxy)**2-(m02)**2)/(2*m01*mxy)
					vA=math.acos(vA)
					vA=math.degrees(vA)
					vA=180-vA

#					print "m01: "+str(m01)+" m02: "+str(m02)+" mxy: "+str(mxy)
					cv2.putText(frame,str(vA), (170,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,255,0])
					a=coord1[0]-coord2[0]
					b=coord1[1]-coord2[1]
					c=point[0]-coord1[0]
					d=point[1]-coord1[1]

					x , y , xd , yd = 0 , 0 , 0 , 0

					if a==0:
						x=1
					else:
						x = a/abs(a)
					if c==0:
						xd=1
					else:
						xd = c/abs(c)
					if b==0:
						y=1
					else:
						y = b/abs(b)
					if d==0:
						yd=1
					else:
						yd = d/abs(d)

#					print "a: ",a," b: ",b," c: ",c," d: ",d
#					print "x: ",x," xd: ",xd," y: ",y," yd: ",yd
#					print ""











					if point[0]>0 and point[1]>0 and not band:
						if abs(vA)<15:
							if m01 > 20:
								print "Avanzar"
							else:
								print "Detente"
						else:
							band = True
							if coord1[1] < coord2[1]:
								if coord1[0] < point[0]:
									print "Girar Derecha 1"
								else:
									print "Girar Izquierda 1"
							else:
								if coord1[0] < point[0]:
									print "Girar Izquierda 2"
								else:
									print "Girar Derecha 2"

					if band:
						if vA < 15:
							band = False
















					cv2.line(frame,(coord1[0],coord1[1]),(point[0],point[1]),(255,0,0),1)
					cv2.line(frame,(coord2[0],coord2[1]),(coord1[0],coord1[1]),(0,0,255),1)

					# Posiciones angulos y datos
					ms1="G:"+str(coord1)
					ms2="R:"+str(coord2)
					ms3="x:"+str(a)
					ms4="y:"+str(b)
					ms5="Obj:"+str(point)
					ms6="xd:"+str(c)
					ms7="yd:"+str(d)
					ms8="Dis:"+str(m01)

					# Mensajes en pantalla (Informacion)
					cv2.putText(frame,ms1, (15,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms2, (15,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms3, (150,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms4, (150,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms5, (15,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms6, (150,215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms7, (150,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
					cv2.putText(frame,ms8, (230,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,0,0])

			cv2.imshow('Camera',frame)
			cv2.imshow('Frente',thresh_cp1)
			cv2.imshow('Espalda',thresh_cp2)
			ant_vA = vA
			ret, img = cap.read()
			img = cv2.flip(img,1)
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break

def main(robotIP,robotPort,url):
	cam = Cam()
	cam.Main()

if __name__ == "__main__":
	# IP de la camara/imagen y Puerto-IP del robot
	url = 'http://192.168.0.100/image'
	robotIp = "148.226.221.158"
	robotPort = 9559
	main(robotIp,robotPort,url)
