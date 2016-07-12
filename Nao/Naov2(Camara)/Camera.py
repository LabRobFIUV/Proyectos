import rospy
from std_msgs.msg import Int32
import predictor as pd
import numpy as np
import cv2
from time import time
import requests
import threading
import urllib
from threading import Thread, Event, ThreadError

global track
pub = rospy.Publisher('CM',Int32,queue_size=4)

class Cam():
	def __init__(self,lower,upper):
		self.lower = lower
		self.upper = upper
		self.stream = requests.get("http://192.168.0.100/image", stream = True)
		self.thread_cancelled = False
		self.thread = Thread(target = self.run)
		self.video = cv2.VideoWriter('video.avi',cv2.cv.CV_FOURCC('M','J','P','G'),20,(320,240),True)
		self.points = []
		self.data = []
		self.tpos = []
		self.yAxis = []
		self.yAxis_view = []
		self.n_data = 0
		self.thresh = 500

	def Search(self):
		n = 15
		thresh = 70

		predict = pd.Predictor()
		predict.add_data(self.tpos)
		predict.plot()

		res = 0
		for j in range(1,n):
			res = res + abs(predict.yAxis[-j] - self.data[-j][1])
		print "el resultado es:",res," con:",len(predict.yAxis)," datos"
		if res < thresh:
			self.yAxis = predict.yAxis
			self.n_data = len(self.tpos)
			print "EL NUMERO DE DATOS ES:",self.n_data
#		self.yAxis = predict.yAxis

	def Search2(self):
		n = 15

		predict = pd.Predictor()
		predict.add_data(self.data)
		predict.plot()

		res = 0
		for j in range(1,n):
			res = res + abs(predict.yAxis[-j] - self.data[-j][1])
		print "el resultado es:",res," con:",len(predict.yAxis)," datos"
		if res < self.thresh:
			self.yAxis = predict.yAxis
			self.n_data = len(self.tpos)
			self.thresh = res
			print "EL NUMERO DE DATOS ES:",self.n_data
		self.yAxis_view = predict.yAxis

	def start(self):
		self.thread.start()

	def run(self):
		bytes = ''
		ant = [0,0,0]
		count, begin = 0, 0
		yAxis = []
		while not self.thread_cancelled:
			try:
				# Toma y conversion de la imagen a formato estandar (inicio)
				bytes+= self.stream.raw.read(1024)
				a = bytes.find('\xff\xd8')
				b = bytes.find('\xff\xd9')

				if a!=-1 and b!=-1:	# Si hubo exito en la captura
					jpg = bytes[a:b+2]
					bytes = bytes[b+2:]
					# Convierte la imagen
					img =  cv2.imdecode(np.fromstring(jpg, dtype = np.uint8),cv2.IMREAD_COLOR)
					# Toma y conversion de la imagen a formato estandar (fin)
					frame = cv2.blur(img,(3,3))

					hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)	# Conversion a HSV
					thresh = cv2.inRange(hsv,self.lower,self.upper)	# Aplicacion de threshold
					thresh = cv2.medianBlur(thresh,7)	# Se aplica filtro de la media
					thresh2 = thresh.copy()	# Copa de thresh

					# Se buscan contornos
					countours, _ = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
					max_area = 0
					best_cnt = 0
					area = 0

					# Se busca el contorno con el mayor area, filtra el ruido
					for cnt in countours:
						area = cv2.contourArea(cnt)
						if area > max_area:
							max_area = area
							best_cnt = cnt

					# Se obtiene el centro del contorno usando momentos
					cx,cy=0,0
					try:
						M = cv2.moments(best_cnt)
						cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
					except:
						self.end_cam()

					# Se almacena la posicion
					coord = cx, cy
					if not (coord in self.points):
						if (cx != 0):
							self.points.append(coord)

					# Se dibuja el desplazamiento
					w = len(self.points)
					for i in range(0,w-1):
						cv2.line(frame, (self.points[i]),(self.points[i+1]),(255,0,0),1)

					# Se dibuja el area de interes
					w = len(self.data)
					for i in range(0,w-1):
						cv2.line(frame, ((self.data[i][0],self.data[i][1])),((self.data[i+1][0],self.data[i+1][1])),(0,0,255),1)

					# Se almacena posiciones del area de interes y el tiempo
					if cx>ant[0] and cy!=ant[1] and 200>=cx>=90:
						if begin == 0:
							begin = cx
						ant[0] = cx
						ant[1] = cy
						t2 = int(str(rospy.Time.now()))
						ta = float(t2)/1000000000.0
						self.data.append([cx,cy])
						self.tpos.append([ta,cy])
						count = count + 1

					if count > 14 and cx<=200 and count != ant[2]:
						ant[2] = count
#						if self.n_data == 0:
#							self.Search2()
						self.Search2()

					if len(self.yAxis)>0:
						posH=begin
						for i in range(len(self.yAxis_view)-1):
							cv2.line(frame,((posH,self.yAxis_view[i])),((posH+1,self.yAxis_view[i+1])),(255,255,0),1)
							posH=posH+1

						posH=begin
						for i in range(len(self.yAxis)-1):
							cv2.line(frame,((posH,self.yAxis[i])),((posH+1,self.yAxis[i+1])),(0,255,255),1)
							posH=posH+1


#					print len(self.data)," ",self.data
#					print "\n"
#					print len(self.yAxis)," ",self.yAxis
					self.video.write(frame)
					cv2.imshow('Objeto',thresh2)
					cv2.imshow('Camara',frame)

					if cv2.waitKey(1) == 1048603:
						self.end_cam()
			
			except ThreadError:
				self.thread_cancelled = True

	def is_running(self):
		return self.thread.isAlive()

	def shut_down(self):
		self.thread_cancelled =  True
		while self.thread.isAlive():
			continue
		return True

	def end_cam(self):
		self.video.release()
		self.thread_cancelled = True
		cv2.destroyAllWindows()

	def move_camera(self):
		abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"
		for i in range(0,3):
			content = urllib.urlopen(abajo).read()

def Opciones(data):
	global track
	c=data.data
	if c==100:
		pub.publish(102)
	if c==1:
		track.start()		# Inicia el procesamiento
		pub.publish(11)		# Publica a "CM" que esta listo
	if c==2:
		track.end_cam()		# Termina y almacena datos

def main():
	rospy.init_node('Camera', anonymous=True)	# Inicia un nodo llamado "Camera"
	rate = rospy.Rate(10)
	rospy.Subscriber("CC", Int32, Opciones)		# Se suscribe al nodo "CC"
	rate.sleep()
	rospy.spin()

if __name__ == '__main__':
	global track
	# Instancia la clase Cam, pasandole el min y max threshold en (V,H,S). Es una variable global
	track=Cam(np.array([120,127,57]),np.array([180,255,255]))
	main()