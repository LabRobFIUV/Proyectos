# Bibliotecas necesarias
import cv2
import time
import math
import urllib
import motion
import requests
import threading
import numpy as np
from naoqi import ALProxy
from threading import Thread, Event, ThreadError

# punto de la pantalla donde se hizo click
point = [0,0]

# Funcion que pone de pie al Nao
def Parar():
    motionProxy.stiffnessInterpolation("Body",1,1.0)
    postureProxy.goToPosture("StandInit",1)

# Funcion que pone al Nao en postura de descanso
def Sentar():
    postureProxy.goToPosture("Crouch",1)
    motionProxy.stiffnessInterpolation("Body",0,1.0)

# Funcion que pone al Nao a caminar indeterminadamente
def Caminar():
    motionProxy.setWalkTargetVelocity(0.6,0,0,0.1)

# Funcion que deteniene la caminata
def Deternerse():
    motionProxy.setWalkTargetVelocity(0,0,0,0)

# Funcion que establece la posicion donde se hizo click
def mousePosition(event,x,y,flags,param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        point = [x,y]

# Clase principal
class Cam():
    # Inicializa las variables para los hilos y la camara
    def __init__(self, url):
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        print "camera initialised"

    # Funcion default
    def nothing(self, x):
        pass

    # Inicia el hilo de la camara
    def start(self):
        self.thread.start()
        print "camera stream started"

    # Funcion principal de la clase
    def run(self):
        bytes=''
        points = []
#        cv2.namedWindow('Camera',cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow('Camera',0)
        cv2.resizeWindow("Camera", 1000,750);
        cv2.setMouseCallback('Camera',mousePosition)
        band = False
        Gband =False

        while not self.thread_cancelled:
            try:
                bytes+=self.stream.raw.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]

                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                    frame = cv2.blur(img,(3,3))
#                    thresh_cp1 = 0
#                    thresh_cp2 = 0

                    battery="Battery:"+str(batteryProxy.getBatteryCharge())+"%"
                    cv2.putText(frame,battery, (230,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,0,0])

                    if point[0]!=0 and point[1]!=0:
                        frame[point[1]-1:point[1]+1,point[0]-1:point[0]+1]=[0,0,255]
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        lower_c1 = np.array([54,37,125])
                        upper_c1 = np.array([85,219,255])
                        lower_c2 = np.array([123,92,97])
                        upper_c2 = np.array([180,173,153])

                        thresh_c1 = cv2.inRange(hsv,lower_c1,upper_c1)
                        thresh_c1 = cv2.medianBlur(thresh_c1,7)
                        thresh_c2 = cv2.inRange(hsv,lower_c2,upper_c2)
                        thresh_c2 = cv2.medianBlur(thresh_c2,7)

                        thresh_cp1 = thresh_c1.copy()
                        thresh_cp2 = thresh_c2.copy()
                        countours_c1, _ = cv2.findContours(thresh_c1, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                        countours_c2, _ = cv2.findContours(thresh_c2, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

                        max_area_c1, max_area_c2 = 0 , 0
                        best_cnt_c1, best_cnt_c2 = 0 , 0
                        area = 0
                        tc1=len(countours_c1)
                        tc2=len(countours_c2)
                        tcm = 0
                        if tc1>tc2:
                            tcm=tc1
                        else:
                            tcm=tc2
                        for i in range(tcm):
                            if i<tc1 and cv2.contourArea(countours_c1[i])>max_area_c1:
                                max_area_c1 = cv2.contourArea(countours_c1[i])
                                best_cnt_c1 = countours_c1[i]
                            if i<tc2 and cv2.contourArea(countours_c2[i])>max_area_c2:
                                max_area_c2 = cv2.contourArea(countours_c2[i])
                                best_cnt_c2 = countours_c2[i]
                        M = cv2.moments(best_cnt_c1)
                        M2 = cv2.moments(best_cnt_c2)

                        coord1 = []
                        coord2 = []
                        try:
                            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                            coord1.append(cx)
                            coord1.append(cy)
                            cx,cy = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])
                            coord2.append(cx)
                            coord2.append(cy)
                        except:
                            coord1.append(0)
                            coord1.append(0)
                            coord2.append(0)
                            coord2.append(0)

                        # OBTERNER DISTANCIAS
                        m01=((coord1[0]-point[0])**2+(coord1[1]-point[1])**2)
                        m01=m01**0.5
                        m02=((coord2[0]-point[0])**2+(coord2[1]-point[1])**2)
                        m02=m02**0.5
                        mxy=((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2)
                        mxy=mxy**0.5


                        vA=((m01)**2+(mxy)**2-(m02)**2)/(2*m01*mxy)
                        vA=math.acos(vA)
                        vA=math.degrees(vA)
                        vA=180-vA
#                        print "m01: "+str(m01)+" m02: "+str(m02)+" mxy: "+str(mxy)
                        cv2.putText(frame,str(vA), (170,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,255,0])

                        a=coord1[0]-coord2[0]
                        b=coord1[1]-coord2[1]
                        c=point[0]-coord1[0]
                        d=point[1]-coord1[1]

                        x , y , xd , yd = 0 , 0 , 0 , 0
                        if a==0:
                            x=1
                        else:
                            x = a/abs(a)
                        if c==0:
                            xd=1
                        else:
                            xd = c/abs(c)
                        if b==0:
                            y=1
                        else:
                            y = b/abs(b)
                        if d==0:
                            yd=1
                        else:
                            yd = d/abs(d)

                        if point[0]!=0 and point[1]!=0:
                            if Gband:
                                if abs(vA)<5:
                                    Gband = False
                                    motionProxy.setWalkTargetVelocity(0,0,0,0)
                            else:
                                if abs(vA)>15: 
                                    if x!=xd and y!=yd:
                                        print "Girar y calcular"
                                    elif x==xd and y==yd:
                                        print "Mismo cuadrante"
#                                        motionProxy.setWalkTargetVelocity(0.5,0,0,0.2)
                                    else:
                                        Gband = True
                                        if x==xd and x>0:
                                            if coord1[1]>point[1]:
                                                print "Girar izquierda 1"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,0.2,0.5)
                                            else:
                                                print "Girar derecha 1"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,-0.2,0.5)
                                        if x==xd and x<0:
                                            if coord1[1]>point[1]:
                                                print "Girar izquierda 2"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,0.2,0.5)
                                            else:
                                                print "Girar derecha 2"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,-0.2,0.5)
                                        if y==yd and y>0:
                                            if coord1[0]>point[0]:
                                                print "Girar derecha 3"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,-0.2,0.5)
                                            else:
                                                print "Girar izquierda 3"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,0.2,0.5)

                                        if y==yd and y<0:
                                            if coord1[0]>point[0]:
                                                print "Girar izquierda 4"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,0.2,0.5)
                                            else:
                                                print "Girar derecha 4"
                                                stiffness=motionProxy.getStiffnesses("Body")
                                                if stiffness[0]==0.0:
                                                    Parar()
                                                motionProxy.setWalkTargetVelocity(0,0,-0.2,0.5)
                                '''
                                else:
                                    if m01>15 and not band:
                                        stiffness=motionProxy.getStiffnesses("Body")
                                        if stiffness[0]==0.0:
                                            Parar()
                                        motionProxy.moveInit()
                                        motionProxy.setWalkTargetVelocity(1.0,0.0,0,0.5)
                                        print "Avanzar"
                                        band = True
                                    if m01<15:
                                        Deternerse()
                                        Sentar()
                                        print "Detener"
                                        band = False
                                        point[0]=0
                                        point[1]=0
                                '''

                        cv2.line(frame,(coord1[0],coord1[1]),(point[0],point[1]),(255,0,0),1)
                        cv2.line(frame,(coord2[0],coord2[1]),(coord1[0],coord1[1]),(0,0,255),1)

                        # Posiciones angulos y datos
                        ms1="G:"+str(coord1)
                        ms2="R:"+str(coord2)
                        ms3="x:"+str(a)
                        ms4="y:"+str(b)
                        ms5="Obj:"+str(point)
                        ms6="xd:"+str(c)
                        ms7="yd:"+str(d)
                        ms8="Dis:"+str(m01)

                        # Mensajes en pantalla (Informacion)
                        cv2.putText(frame,ms1, (15,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms2, (15,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms3, (150,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms4, (150,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms5, (15,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms6, (150,215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms7, (150,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,ms8, (230,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,0,0])

                    # Muestra la imagen y detente con Esc
                    cv2.imshow('Camera',frame)
#                    cv2.imshow('Verde',thresh_cp1)
#                    cv2.imshow('Azul',thresh_cp2)
                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        break

            # Si hay un error deten todo
            except ThreadError:
                self.thread_cancelled = True

    # Sigue en marcha el hilo
    def is_running(self):
        return self.thread.isAlive()
        
    # Detener el funcionamiento de los hilos
    def shut_down(self):
        self.thread_cancelled = True
        while self.thread.isAlive():
            time.sleep(1)
        return True

    # Mueve la perspectica de la camara hacia abajo
    def move_camera(self):
        abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"
        for x in range(0,3):
            content = urllib.urlopen(abajo).read()

def main(robotIP,robotPort,url):
    # Herramientas necesarias [Bateria es opcional]
    global batteryProxy
    global motionProxy
    global postureProxy
    try:
        batteryProxy = ALProxy("ALBattery", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALBattery"
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"

    # Mover brazos con caminata y levantar al Nao lo detiene
    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    # Instancia de la clase, colocar camara e iniciar
    cam = Cam(url)
    cam.move_camera()
    cam.start()

if __name__ == "__main__":
    # IP de la camara/imagen y Puerto-IP del robot
    url = 'http://192.168.0.100/image'
    robotIp = "148.226.221.158"
    robotPort = 9559
    main(robotIp,robotPort,url)
