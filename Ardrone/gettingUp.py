import numpy as np
import cv2
import cv
import libardrone
import time as t

def main():
	segundos = 5
	drone = libardrone.ARDrone(True)
	drone.reset()
	drone.set_camera_view(1)
	print "Presiona U para subir"
	drone.speed = 0.1
	i = 1

	while True:
		running = True

		try:
			start = t.time()
			frame = drone.get_image()
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			cv2.imshow('frame',frame)
			bat = drone.navdata.get(0, dict()).get('battery', 0)
			alt = drone.navdata.get(0, dict()).get('altitude', 0)
			print "Bateria:" + str(bat)
			print "\nAltura" + str(alt)
			tecla = cv2.waitKey(15)
			
			if (tecla > 0):
				print tecla

			#Tecla P / Take photo
			if (tecla == 1048603) and (running == True):
				print "P"
				cv2.imwrite("photo-" + str(i) + ".jpeg",frame)
				i+=1
				print i
				running = False
			#Tecla U / Subir
			elif (tecla == 1048693):
				print "Subiendo"
				while (t.time() < start + segundos) and (running == True):
					print "subiendo"
				running = False
				print "acabo"
			#Tecla W / Move Forward
			elif (tecla == 1048695):
				print "W"
				#drone.move_forward()
			#Tecla A / Move Left
			elif (tecla == 1048673):
				print "A"
				#drone.move_left()
			#Tecla S / Move Back
			elif (tecla == 1048691):
				print "S"
				#drone.move_backward()
			#Tecla D / Move Right
			elif (tecla == 1048676):
				print "D"
				#drone.move_right()

			#Tecla Up / Up
			elif (tecla == 1113938):
				print "Arriba"
				#drone.move_up()
			#Tecla Down / Down
			elif (tecla == 1113940):
				print "Abajo"
				#drone.move_down()
			#Tecla Right / Turn Right
			elif (tecla == 1113939):
				print "Derecha"
				#drone.turn_right()
			#Tecla Left / Turn Left
			elif (tecla == 1113937):
				print "Izquierda"
				#drone.turn_left()
			#Tecla Space / Land
			elif (tecla == 1048608):
				print "Espacio"
				#drone.land()
			#Tecla Enter / Takeoff
			elif (tecla == 1048586):
				print "Enter"
				#drone.takeoff()
			#Tecla Backspace / Emergency
			elif (tecla == ):
				print "Borrar"
				#drone.reset()
			#Escape
			elif (tecla == 1048603):
				cv2.destroyAllWindows()
				drone.reset()
				drone.halt()
				break
		except:
			pass

if __name__ == '__main__':
	main()