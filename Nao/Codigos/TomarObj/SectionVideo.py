import numpy as np
import cv2
import time

class GetVideos():
	def __init__(self,lower_c,upper_c,name='video.avi'):
		self.name=name
		self.lower_c=lower_c
		self.upper_c=upper_c
		self.video = cv2.VideoWriter('Cut_'+self.name,cv2.cv.CV_FOURCC('M','J','P','G'),20,(320,240),True)
		self.val=0
		self.posIni = 0
		self.posFin = 0

	def Cut(self):
		cap = cv2.VideoCapture(self.name)
		points = []

		p, frame = cap.read()
		while p:
			hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			thresh = cv2.inRange(hsv,self.lower_c,self.upper_c)
			thresh = cv2.medianBlur(thresh,7)
			thresh2 = thresh.copy()
			countours, _ = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
			self.val = self.val + 1
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
				print "Error. Seguimiento incompleto"
				break

			if 200>cx>100:
				try:
					if self.posIni==0:
						self.posIni = self.val -1
					band=True
					self.video.write(frame)
				except:
					print"Error con el frame, saltando..."
			if cx>=200 and self.posFin==0:
				self.posFin = self.val -1

			p, frame = cap.read()
		cap.release()