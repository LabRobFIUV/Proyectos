import predictor as pd
import numpy as np
import rospy
import cv2
import sys
import time
import os

class Cam():
        def __init__(self,lower,upper,name="video.avi"):
                self.name = name
                self.lower = lower
                self.upper = upper
                self.points = []
                self.data = []
                self.tpos = []
                self.img = 0
                self.img_temp = 0
                self.begin = 0
                self.n_data = 0

        def Search(self):
                n = 15
                thresh = 85
                predict = pd.Predictor()
                for i in range(len(self.data)):
                        if len(self.tpos[:i]) > (n-1):
                                res = 0
                                predict.add_data(self.tpos[:i])
                                predict.plot()
                                for j in range(1,n):
                                        t = self.data[:i]
                                        res = res + abs(predict.yAxis[-j] - t[-j][1])
                                if res < thresh:
                                        self.n_data = len(self.tpos[:i])
                                        print "EL NUMERO DE DATOS ES:",self.n_data
                                        break

        def Analize(self):
                ant=[0,0]
                cap = cv2.VideoCapture(self.name)
                ret, frame = cap.read()
                self.img = frame
                while ret:
                        frame = cv2.blur(frame,(3,3))
                        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                        thresh = cv2.inRange(hsv,self.lower,self.upper)
                        thresh = cv2.medianBlur(thresh,7)

                        countours, _ = cv2.findContours(thresh, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                        max_area = 0
                        best_cnt = 0
                        area = 0

                        for cnt in countours:
                                area = cv2.contourArea(cnt)
                                if area > max_area:
                                        max_area = area
                                        best_cnt = cnt

                        cx,cy = 0,0
                        try:
                                M = cv2.moments(best_cnt)
                                cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                        except:
                                pass

                        coord = cx, cy
                        if not (coord in self.points):
                                if (cx != 0):
                                        self.points.append(coord)

                        if cx>ant[0] and 200>=cx>=90 and cy!=ant[1]:
                                ant[0] = cx
                                ant[1] = cy
                                t2 = int(str(rospy.Time.now()))
                                ta = float(t2)/1000000000.0
                                self.data.append([cx,cy])
                                self.tpos.append([ta,cy])

                        # TACKING
                        w = len(self.points)
                        for i in range(0,w-1):
                                cv2.line(frame, (self.points[i]),(self.points[i+1]),(255,0,0),1)

                        #time.sleep(0.03)
                        cv2.imshow('Camara',frame)
                        k = cv2.waitKey(1)
                        if k == 1048603:
                                exit(0)
                        if k == 1048688:
                                cv2.imwrite('image.png',frame)
                        ret, frame = cap.read()
                cv2.destroyAllWindows()

        def end_cam(self):
                global data, data2, tdata, tdata2, band
                f = open('posiciones[x,y].txt','wa')
                for i in range(0,len(data2)):
                        f.write(str(data2[i][0]) + " " + str(data2[i][1]) + "\n")
                g = open('posiciones.txt','wa')
                for i in range(0,len(self.points)):
                        g.write(str(self.points[i][0]) + " " + str(self.points[i][1]) + "\n")
                cv2.destroyAllWindows()

        def View(self):
                global data, data2, tdata, tdata2, band
                begin = 0
                num_data = 0
                cv2.namedWindow('Result',cv2.CV_WINDOW_AUTOSIZE)
                cv2.createTrackbar('N_datos', 'Result', num_data, 60, self.update)
                cv2.createTrackbar('Begin', 'Result', begin, 60, self.update)

                self.img_temp = self.img.copy()
                predict = pd.Predictor()
                data = self.data[:]
                data2 = self.data[:]
                tdata = self.tpos[:]
                tdata2 = self.tpos[:]

                # TACKING
                w = len(self.points)
                for i in range(0,w-1):
                        cv2.line(self.img, (self.points[i]),(self.points[i+1]),(255,0,0),1)

                w = len(self.data)
                for i in range(0,w-1):
                        cv2.line(self.img, ((self.data[i][0],self.data[i][1])),((self.data[i+1][0],self.data[i+1][1])),(0,0,255),1)
                cv2.setTrackbarPos("N_datos","Result", self.n_data)

                while True:
                        begin = cv2.getTrackbarPos('Begin','Result') + 90
                        num_data = cv2.getTrackbarPos('N_datos','Result')

                        cv2.line(self.img_temp, (begin,0), (begin,240),(200,200,200),1)
                        cv2.line(self.img_temp, (begin+num_data,0), (begin+num_data,240),(20,20,20),1)

                        if band == False and num_data>2:
                                predict.add_data(tdata2)
                                predict.plot()
                                band = True

                        if len(predict.yAxis)>0:
                                posH=begin
                                for i in range(len(predict.yAxis)-1):
                                        posH=posH+1
                                        try:
                                                if posH>(begin+num_data):
                                                        cv2.line(self.img_temp,((posH,predict.yAxis[i])),((posH+1,predict.yAxis[i+1])),(255,0,0),1)
                                                else:
                                                        cv2.line(self.img_temp,((posH,predict.yAxis[i])),((posH+1,predict.yAxis[i+1])),(0,255,255),1)
                                        except:
                                                pass

                        cv2.imshow('Result',self.img_temp)
                        k = cv2.waitKey(1)
                        if k == 1048688:
                                cv2.imwrite("image2.png",self.img_temp)
                        if k == 1048603:
                                self.end_cam()
                                break

        def update(self,y):
                global data, data2, tdata, tdata2, band
                ptr = []
                self.img_temp = self.img.copy()
                for i in range(len(self.data)):
                        x = cv2.getTrackbarPos('Begin','Result')
                        if (self.data[i][0]>=(x+90)):
                                v = cv2.getTrackbarPos('N_datos','Result')
                                if len(self.data[i:]) > v:
                                        #os.system('clear')
                                        j = len(self.data[i:]) - v
                                        #print "v: ",v," j: ",j," i: ",i," n_data:",len(self.data),"\ndata[i]:",self.data[i],"num:",len(self.data[i:-j])
                                        data = self.data[i:-j]
                                        tdata = self.tpos[i:-j]
                                        ptr.append(self.data[i:-j])
                                        ptr.append(self.tpos[i:-j])
                                        #print len(data2)
                                        #print self.data[i:-j]
                                        break
                data2 = data[:]
                tdata2 = tdata[:]
                band = False
                self.View_Result(ptr)

        def View_Result(self,ptr):
                os.system('clear')
                n = 15
                if len(ptr[0]) > (n-1):
                        predict = pd.Predictor()

                        res = 0
                        predict.add_data(ptr[1])
                        predict.plot()
                        print ptr[0]
                        print "\n"
                        for j in range(1,n):
                                t = ptr[0]
                                res = res + abs(predict.yAxis[-j] - t[-j][1])
                        print predict.yAxis
                        print res

def main():
        global data, data2, tdata, tdata2, band
        rospy.init_node('Camera', anonymous=True)

        track = ""
        if len(sys.argv)>1:
                track=Cam(np.array([120,90,63]),np.array([180,255,255]),sys.argv[1])
                print sys.argv[1]
        else:
                track=Cam(np.array([120,90,63]),np.array([180,255,255]))

        band = False
        track.Analize()
        track.Search()
        track.View()

if __name__ == '__main__':
        main()
