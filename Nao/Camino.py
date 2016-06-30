import numpy as np
import cv,cv2

def Muros(img,img2,tam):
	a=img.shape
	for i in range(a[0]):
		for j in range(a[1]):
			if img[i][j]==0:
				try:
					img2[i][j-2]=0
					img2[i][j-1]=0
					img2[i][j]=0
					img2[i][j+1]=0
					img2[i][j+2]=0
				except IndexError:
					pass
	for i in range(a[1]):
		for j in range(a[0]):
			if img[i][j]==0:
				try:
					img2[j][i+1]=0
					img2[j][i+2]=0
					img2[j][i+3]=0
					img2[j][i+4]=0
				except IndexError:
					pass
	cv2.imshow('Prueba2',img2)
	cv2.imshow('Prueba',img)
	cv2.waitKey()

def Limit(self,posact):
	a=posact[0]-(tam-1)/2
	p=self.Traduccion(posact)
	try:
		if self.virtualspace[p[0]][p[1]][1]==True:
			return True
	except IndexError, e:
		return True

	try:
		for x in range(self.tam):
			b=posact[1]-(tam-1)/2
			for y in range(self.tam):
				if self.mapi[a,b]==0:
					self.virtualspace[p[0]][p[1]][0]=-1
					self.virtualspace[p[0]][p[1]][1]=True
					return True
				b=b+1
			a=a+1
		return False
	except IndexError, e:
		print "Fuera del area"
		return True

def Traduccion(self,pos):
	dim=self.mapi.shape
	a=int(pos[0]/self.tam)
	b=int(pos[1]/self.tam)
	return [a,b]

def Marcar(self,pos):
	for i in range(int(self.tam*.25)):
		for j in range(int(self.tam*.25)):
			a=i+pos[0]-int(tam/8)
			b=j+pos[1]-int(tam/8)
			self.mapi[a,b]=127
	#cv2.imshow('Prueba',self.mapi)
	#cv2.waitKey()


def Expand(self,pos,lsi):
	#self.Marcar(pos)
	a=self.Traduccion(pos)

	val=self.virtualspace[a[0]][a[1]][0]
	if not self.Limit([pos[0]+self.tam,pos[1]]):
		a=self.Traduccion([pos[0]+self.tam,pos[1]])
		self.virtualspace[a[0]][a[1]][0]=val+1
		self.virtualspace[a[0]][a[1]][1]=True
		lsi.append([pos[0]+self.tam,pos[1]])

	if not self.Limit([pos[0],pos[1]+self.tam]):
		a=self.Traduccion([pos[0],pos[1]+self.tam])	
		self.virtualspace[a[0]][a[1]][0]=val+1
		self.virtualspace[a[0]][a[1]][1]=True
		lsi.append([pos[0],pos[1]+self.tam])

	if not self.Limit([pos[0]-self.tam,pos[1]]):
		a=self.Traduccion([pos[0]-self.tam,pos[1]])
		self.virtualspace[a[0]][a[1]][0]=val+1
		self.virtualspace[a[0]][a[1]][1]=True
		lsi.append([pos[0]-self.tam,pos[1]])

	if not self.Limit([pos[0],pos[1]-self.tam]):
		a=self.Traduccion([pos[0],pos[1]-self.tam])	
		self.virtualspace[a[0]][a[1]][0]=val+1
		self.virtualspace[a[0]][a[1]][1]=True
		lsi.append([pos[0],pos[1]-self.tam])

	a=self.Traduccion(pos)
	n=self.Traduccion(self.posfin)

	if a==n:
		return True
	else:
		return False

def MRoad(self):
	self.road.append(self.posfin)
	pos=self.posfin
	a=self.Traduccion(pos)
	val=self.virtualspace[a[0]][a[1]][0]

	while val>0:
		print "pos:  "+str(pos)

		b=self.virtualspace[a[0]+1][a[1]][0]
		c=self.virtualspace[a[0]-1][a[1]][0]
		d=self.virtualspace[a[0]][a[1]+1][0]
		e=self.virtualspace[a[0]][a[1]-1][0]

		menor=1000
		vpn=[]

		if b>=0:
			menor=b
			vpn=[pos[0]+self.tam,pos[1]]

		if c>=0:
			if c<menor:
				menor=c
				vpn=[pos[0]-self.tam,pos[1]]

		if d>=0:
			if d<menor:
				menor=d
				vpn=[pos[0],pos[1]+self.tam]

		if e>=0:
			if e<menor:
				menor=e
				vpn=[pos[0],pos[1]-self.tam]

		a=self.Traduccion(vpn)
		val=self.virtualspace[a[0]][a[1]][0]
		self.road.append(vpn)
		pos=vpn

def DHCP(pi,pf,img):
	for i in range(self.tam):
		for j in range(self.tam):
			a=i+self.posini[0]-int(tam/2)
			b=j+self.posini[1]-int(tam/2)
			self.mapi[a,b]=63

	for i in range(self.tam):
		for j in range(self.tam):
			a=i+self.posfin[0]-int(tam/2)
			b=j+self.posfin[1]-int(tam/2)
			self.mapi[a,b]=190
	dim=img.shape
	a=int(posini[0]/tam)
	b=int(posini[1]/tam)
	c=int((dim[0]-self.posini[0])/self.tam)	
	d=int((dim[1]-self.posini[1])/self.tam)
#		print dim[0]/tam
#		print dim[1]/tam
#		print a
#		print b
#		print c
#		print d
	# Error de desfasar

	for i in range(a+c):
		self.virtualspace.append([])

	for i in range(a+c):
		for j in range(b+d):
			self.virtualspace[i].append([0,False]) 

	lista=[]
	lista1=[]
	lista.append(self.posini)
	self.virtualspace[a][b][1]= True

	est=False
	while not est:
		for i in lista:
			est=self.Expand(i,lista1)
			if est:
				return

		lista=[]

		for j in lista1:
			est=self.Expand(j,lista)
			if est:
				return
		lista1=[]

def Topic(self):
	self.MRoad()
	self.road.reverse()
	for x in self.road:
		self.Marcar(x)
	cv2.imshow('Prueba',self.mapi)
	cv2.waitKey()

def Salvar(self):
	f = open("2Dpoints","w")
	for i in self.road:
		f.write(str(i)+'\n')
	f.close()

def Convert(pix):
	pix[0]=pix[0]*-1
	a=int(pix[0]*20)+235
	b=int(pix[1]*20)+244
	tam=4
	return [a,b]

if __name__ == '__main__':
	pi=[50,50]
	pf=[100,200]
	tam=4
	img = cv2.imread('a.png',cv.CV_LOAD_IMAGE_GRAYSCALE)
	img2 = cv2.imread('a.png',cv.CV_LOAD_IMAGE_GRAYSCALE)
	Muros(img,img2,tam)
	#resmap.DHCP(pi,pf,img)
	#resmap.Topic()
	#resmap.Salvar()