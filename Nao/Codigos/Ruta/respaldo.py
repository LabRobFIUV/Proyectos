import cv2
import time
import urllib
import motion
import requests
import threading
import numpy as np
from naoqi import ALProxy
from threading import Thread, Event, ThreadError

point = [0,0]
def Parar():
    motionProxy.stiffnessInterpolation("Body",1,1.0)
    postureProxy.goToPosture("StandInit",1)

def Sentar():
    postureProxy.goToPosture("Crouch",1)
    motionProxy.stiffnessInterpolation("Body",0,1.0)

def Caminar():
    motionProxy.setWalkTargetVelocity(0.6,0,0,0.1)

def Deternerse():
    motionProxy.setWalkTargetVelocity(0,0,0,0)

def mousePosition(event,x,y,flags,param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        point = [y,x]
        print point

class Cam():
    def __init__(self, url):
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        print "camera initialised"

    def nothing():
        pass

    def start(self):
        self.thread.start()
        print "camera stream started"
    
    def run(self):
        bytes=''
        points = []
#        cv2.namedWindow('Camera',cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow('Camera',0)
        cv2.resizeWindow("Camera", 1000,750);
        cv2.setMouseCallback('Camera',mousePosition)
        band = False

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

                    if point[0]!=0 and point[1]!=0:
                        frame[point[0]-1:point[0]+1,point[1]-1:point[1]+1]=[0,0,255]
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        lower_c1 = np.array([41,62,156])
                        upper_c1 = np.array([91,156,237])
                        lower_c2 = np.array([130,28,84])
                        upper_c2 = np.array([180,171,185])

                        thresh_c1 = cv2.inRange(hsv,lower_c1,upper_c1)
                        thresh_c1 = cv2.medianBlur(thresh_c1,7)
                        thresh_c2 = cv2.inRange(hsv,lower_c2,upper_c2)
                        thresh_c2 = cv2.medianBlur(thresh_c2,7)

#                        thresh_cp1 = thresh_c1.copy()
#                        thresh_cp2 = thresh_c2.copy()
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
                        '''
                        for cnt in countours_c1:
                            area = cv2.contourArea(cnt)
                            if area > max_area_c1:
                                max_area_c1 = area
                                best_cnt_c1 = cnt
                        for cnt in countours_c2:
                            area = cv2.contourArea(cnt)
                            if area > max_area_c2:
                                max_area_c2 = area
                                best_cnt_c2 = cnt
                        '''
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
                        m01=((coord1[0]-point[1])**2+(coord1[1]-point[0])**2)
                        m01=m01**0.5
                        m02=((coord2[0]-point[1])**2+(coord2[1]-point[0])**2)
                        m02=m02**0.5

                        if point[0]!=0 and point[1]!=0:
                            if m01>15 and not band:
#                                Parar()
#                                motionProxy.moveInit()
#                                motionProxy.setWalkTargetVelocity(1.0,0.0,-0.01,0.5)
                                print "Avanzar"
                                band = True
                            if m01<15:
#                                Deternerse()
#                                Sentar()
                                print "Detener"
                                band = False
                                point[0]=0
                                point[1]=0

                        cv2.line(frame,(coord1[0],coord1[1]),(point[1],point[0]),(255,0,0),1)
                        cv2.line(frame,(coord2[0],coord2[1]),(point[1],point[0]),(0,255,),1)

                        cv2.putText(frame,"Azul: "+str(m01), (15,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])
                        cv2.putText(frame,"Verde: "+str(m02), (15,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0,0,255])

                    cv2.imshow('Camera',frame)
                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        break

            except ThreadError:
                self.thread_cancelled = True

    def is_running(self):
        return self.thread.isAlive()
    
    def shut_down(self):
        self.thread_cancelled = True
        while self.thread.isAlive():
            time.sleep(1)
        return True

    def move_camera(self):
        abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"
        for x in range(0,3):
            content = urllib.urlopen(abajo).read()

def main(robotIP,robotPort,url):
    global motionProxy
    global postureProxy
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"

    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    cam = Cam(url)
    cam.move_camera()
    cam.start()

if __name__ == "__main__":
    url = 'http://192.168.0.100/image'
    robotIp = "148.226.221.158"
    robotPort = 9559
    main(robotIp,robotPort,url)
