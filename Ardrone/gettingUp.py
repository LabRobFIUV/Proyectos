import numpy as np
import cv2
import libardrone
import time as t

def main():
	segundos = 5
	start = t.time()
	drone = libardrone.ARDrone(True)
	drone.reset()
	drone.set_camera_view(1)
	print "Presiona W para subir"
	running = True

	while(1):
		try:
			frame = drone.get_image()
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			cv2.imshow('frame',frame)

			tecla = cv2.waitKey(15)

			#Tecla W
			if (tecla == 1048695):
				while t.time() < start + segundos:
					print "subiendo"
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