import numpy as np
import cv2
import time

hue = 10
sat = 10
val = 10
hue2 = 180
sat2 = 255
val2 = 255

class Cam():
	def Detect(self):
		global hue, sat, val
		points = []
		cap = cv2.VideoCapture(0)
		ret, img = cap.read()

		while(ret):
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


			cv2.imshow('Camera',frame)
			cv2.imshow('Objeto',thresh2)

			ret, img = cap.read()
			if cv2.waitKey(1) ==1048603:
				exit(0)
				f.close()

	def nothing(self,x):
		pass

	cv2.namedWindow('Camera',cv2.CV_WINDOW_AUTOSIZE)
	cv2.namedWindow('Objeto',cv2.CV_WINDOW_AUTOSIZE)
	cv2.createTrackbar('H', 'Objeto', hue, 180, nothing)
	cv2.createTrackbar('S', 'Objeto', sat, 255, nothing)
	cv2.createTrackbar('V', 'Objeto', val, 255, nothing)
	cv2.createTrackbar('H', 'Camera', hue2, 180, nothing)
	cv2.createTrackbar('S', 'Camera', sat2, 255, nothing)
	cv2.createTrackbar('V', 'Camera', val2, 255, nothing)

if __name__ == "__main__":
	cam = Cam()
	cam.Detect()