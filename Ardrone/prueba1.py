import numpy as np
import cv2
import libardrone

def main():
	drone = libardrone.ARDrone(True)
	drone.reset()
	drone.set_camera_view(1)
	running = True

	while(1):
		try:
			frame = drone.get_image()
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			cv2.imshow('frame',frame)

			tecla = cv2.waitKey(15)

			if (tecla == 1048603):
				cv2.destroyAllWindows()
				drone.reset()
				drone.halt()
				break
		except:
			pass

if __name__ == '__main__':
	main()