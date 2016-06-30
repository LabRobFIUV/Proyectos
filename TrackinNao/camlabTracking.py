import cv2
import cv
import numpy as np
import urllib

points =[]
fps = 25
capSize = (320,240) # this is the size of my source video
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
def url_to_image(url):
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image



    
#Teclas orientadas con la camara boca arriba

izquierda = "http://192.168.0.100/command/ptzf.cgi?relative=0610"
derecha = "http://192.168.0.100/command/ptzf.cgi?relative=0410"
arriba = "http://192.168.0.100/command/ptzf.cgi?relative=0210"
abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"
ArD = "http://192.168.0.100/command/ptzf.cgi?relative=0310"
ArI = "http://192.168.0.100/command/ptzf.cgi?relative=0110"
AbD = "http://192.168.0.100/command/ptzf.cgi?relative=0910"
AbI = "http://192.168.0.100/command/ptzf.cgi?relative=0710"
Wide = "http://192.168.0.100/command/ptzf.cgi?relative=1010"
Tele = "http://192.168.0.100/command/ptzf.cgi?relative=1110"
setting = "http://192.168.0.100/command/presetposition.cgi?HomePos"

url2 ="http://192.168.0.100/oneshotimage.jpg"
#image= url_to_image()

video = cv2.VideoWriter('output.avi',fourcc,fps,capSize)

while True:
    
    image = url_to_image(url2)
    frame = cv2.flip(image,-1)

    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #thresh = cv2.inRange(hsv,np.array((160,150, 80)), np.array((179, 255, 255)))
    thresh = cv2.inRange(hsv,np.array((103,150, 150)), np.array((140,255,255)))
    thresh2 = thresh.copy()

    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    best_cnt = 1
    area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # Encuentra el centroide de el cuerpo detectado
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])


    if (cx != 0):
    	points.append((cx,cy))

    w = len(points)
    
    #si no hay nada no guarda coordenadas (0,0)
    for i in range(0,w-1):
    	cv2.line(frame,(points[i]),(points[i+1]),(255,0,0),5)


    video.write(image) 

    cv2.imshow('frame',frame)
    cv2.imshow('thresh',thresh2)


    tecla =cv2.waitKey(15)
    if (tecla>0):
        print tecla

    if (tecla==1048603):#Escape
		print points
		break

    if (tecla==1048695):#W
        content = urllib.urlopen(arriba).read()

    if (tecla==1048696):#X
        content = urllib.urlopen(abajo).read()

    if (tecla==1048673):#A
        content = urllib.urlopen(izquierda).read()

    if (tecla==1048676):#D
        content = urllib.urlopen(derecha).read()

    if (tecla==1048677):#E
        content = urllib.urlopen(ArD).read()

    if (tecla==1048689):#Q
        content = urllib.urlopen(ArI).read()

    if (tecla==1048675):#C
        content = urllib.urlopen(AbD).read()

    if (tecla==1048698):#Z
        content = urllib.urlopen(AbI).read()

    if (tecla==1048691):#S
        content = urllib.urlopen(Wide).read()

    if (tecla==1048694):#V
        content = urllib.urlopen(Tele).read()

    if (tecla==1113939):#->
        content = urllib.urlopen(setting).read()

video.release()
cv2.destroyAllWindows()
