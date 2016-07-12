import numpy as np
import matplotlib.pyplot as plt
from time import time
import os

class Predictor:
	def __init__(self, xAxis=[], yAxis=[]):
		self.historic_x = xAxis
		self.historic_y = yAxis
		self.Am = 0.0
		self.omega = 0.0
		self.Phi = 0.0
		self.yAxis = []

	def add_lecture(self, x, y):
		self.historic_y.append(y)
		self.historic_x.append(x)

	def trap_area(self, b, b2, h):
		return (b + b2) * h / 2

	def myquad(self, x, y):
		if len(x) < 2 or len(y) < 2 or len(x) != len(y):
			return 0
		return self.trap_area(x[0], x[1], y[1] - y[0])

	def integral_t(self, t, y, integral_times=1, potencia_t=1, multiply=False):
		if len(t) != len(y):
			print "t e y tienen valores diferentes"
		t_temp = np.array(t) ** potencia_t
		y_temp = np.array(y)
		I = [0]
		if multiply:
			y_temp *= t_temp

		for i in range(len(t) - 1):
			t_range = np.array(t[i:i + 2])
			y_range = y_temp[i:i + 2]
			I.append(I[i] + self.myquad(y_range, t_range))
		acumulado = I[-1]
		if integral_times > 1:
			acumulado = self.integral_t(t, I, integral_times - 1)
		return acumulado

	def identify(self, time=None, pos=None):
		if not (time and pos):
			time = self.historic_x
			pos = self.historic_y

		t = np.array(time)
		y = np.array(pos)

		a = (t[-1] ** 3) * y[-1]

		b = self.integral_t(time, pos, 1, 2, True)
		c = self.integral_t(time, pos, 2, 1, True)
		d = self.integral_t(time, pos, 3)
		n1 = a - 9 * b + 18 * c - 6 * d
		e = self.integral_t(time, pos, 2, 3, True)
		f = self.integral_t(time, pos, 3, 2, True)
		d1 = -e + 3 * f

		if (d1 == 0):
			self.omega = 0
			self.Am = 0
			self.Phi = 0
			return 0, 0, 0

		P1 = n1 / d1

		a3 = -12 / (t[-1] ** 4)
		g3 = self.integral_t(time, pos, 4, 1, True)
		h3 = self.integral_t(time, pos, 5)
		i3 = self.integral_t(time, pos, 4, 3, True)
		j3 = self.integral_t(time, pos, 5, 2, True)

		P3 = a3*(-a+11*b-28*c+12*d+P1*(-2*e+14*f-20*g3+4*h3)+(P1**2)*(-i3+3*j3))
		P3 = abs(P3)

		a2 = 3 / ((t[-1] ** 3) * P1)
		a2_1 = -t[-1] * y[-1]

		b2 = self.integral_t(time, pos)
		P2 = a2*(a2_1+b2+2*P1*(-c+d)+(P1**2)*(-g3+h3)-P1*P3*((t[-1]**4)/24)+P3*((t[-1] ** 2) / 2))

		self.Am = 0
		self.omega = np.sqrt(abs(P1))
		if (P1 != 0):
			self.Am = np.sqrt(abs((P3 ** 2) / P1 + (P2 ** 2)))
#		self.Phi = np.arctan((P2 * self.omega) / P3)*(-1)
		self.Phi = np.arctan((P2 * self.omega) / P3)

	def predict_value_y(self, x):
		return self.Am * np.sin(self.omega * x + self.Phi)

	def add_data(self, x):
		self.historic_x = []
		self.historic_y = []
		for i in range(len(x)):
			self.historic_x.append(x[i][0])
			self.historic_y.append(x[i][1])

	def show_data(self,offset=None,num=None):
		print "historic_x:"
		print self.historic_x

		print "\nhistoric_y:"
		print self.historic_y

		if offset != None and num != None:
			print "\noffset: ",offset," num: ",num

		print "\nyAxis:"
		print self.yAxis
		print "\nAm: ",self.Am," Phi: ",self.Phi," omega: ",self.omega

	def plot(self):
#		os.system('clear')
		# ENCONTRAR EL TIEMPO ESTIMADO
		val_x=self.historic_x[:]
		x = self.historic_x[0]
		for f in range(len(self.historic_x)):
			self.historic_x[f]=self.historic_x[f]-x

		# CALCULAR PROMEDIO DE POSICIONES
		offset,num = 0,0
		for f in range(len(self.historic_y)):
			offset=offset+self.historic_y[f]
			num=num+1
		offset=offset/num

		# CENTRAR POSICIONES
		val_y=self.historic_y[:]
		for f in range(len(self.historic_y)):
			self.historic_y[f] = int(self.historic_y[f]) - offset

		# ENCONTRAR POSICIONES FUTURAS
		yAxis = []
		self.identify()
		for x in self.historic_x:
			yAxis.append(int(self.predict_value_y(x)))

		# RESTABLECER POSICIONES
		for f in range(len(yAxis)):
			yAxis[f] = int(yAxis[f]) + offset

		# ENCONTRAR MAS POSICIONES (BETA)
#		temp_x=self.historic_x[-1]
#		for x in range(30):
#			temp_x=temp_x+0.1
#			yAxis.append(self.predict_value_y(x))
#		print self.historic_x

		self.yAxis = yAxis
		self.save()
#		self.show_data(offset,num)
		self.historic_x=val_x[:]

	def save(self):
		f = open('posiciones[t,y].txt','wa')
		for i in range(0,len(self.historic_x)):
			f.write(str(self.historic_x[i]) + " " + str(self.historic_y[i]) + "\n")

		g = open('Values.txt','wa')
		g.write("Omega: "+str(self.omega) + " Am: " + str(self.Am) +" Phi: "+ str(self.Phi)+"\n")
