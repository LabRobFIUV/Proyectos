import numpy as np
import cv2
import libardrone
import time as t

def main():
	segundos = 5
	drone = libardrone.ARDrone(True)
	drone.reset()
	drone.set_camera_view(1)
	print "Presiona W para subir"
	

	while True:
		running = True
		
		try:
			start = t.time()
			frame = drone.get_image()
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			cv2.imshow('frame',frame)

			tecla = cv2.waitKey(15)
			
			if (tecla > 0):
				print tecla

			#Tecla W
			if (tecla == 1048695):
				drone.speed = 0.1
				while (t.time() < start + segundos) and (running == True):
					print "subiendo"
				running = False
				print "acabo"
			#Escape
			if (tecla == 1048603):
				cv2.destroyAllWindows()
				drone.reset()
				drone.halt()
				break
		except:
			pass

if __name__ == '__main__':
	main()