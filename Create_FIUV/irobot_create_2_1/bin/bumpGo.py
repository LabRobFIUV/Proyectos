#!/usr/bin/python
import roslib; roslib.load_manifest('irobot_create_2_1')
import rospy
from time import sleep
from threading import Thread

from irobot_create_2_1.msg import SensorPacket
from irobot_create_2_1.srv import *

def recievePacket(data):
        global bumperRef, distanceRef, angleRef
        bumperRef[0] = data.bumpLeft or data.bumpRight
        distanceRef[0] = data.distance
        angleRef[0] = data.angle

class BumpGo(Thread):
        def __init__(self, bumperRef, distanceRef, angleRef):
                Thread.__init__(self)
                self.go = True
                self.bumperRef = bumperRef
                self.distanceRef = distanceRef
                self.angleRef = angleRef

                rospy.wait_for_service('brake')
                self.brake = rospy.ServiceProxy('brake', Brake)

                rospy.wait_for_service('tank')
                self.tank = rospy.ServiceProxy('tank', Tank)

                rospy.wait_for_service('turn')
                self.turn = rospy.ServiceProxy('turn', Turn)

                self.speed = 250

        def run(self):
                try:
                        while(self.go):
                                if (self.bumperRef[0]):
                                        self.brake(1)  
                                        self.tank(1, -1*self.speed,-1*self.speed)
                                        while(self.go and self.distanceRef[0] > -100):
                                                sleep(0.02)
                                        self.brake(1)
                                        self.turn(1,50)
                                        while(self.go and self.angleRef[0] > -18):
                                                sleep(0.03)
                                        self.brake(1)
                                else:
                                        self.tank(0, self.speed,self.speed)
                                sleep(0.03)
                        self.brake(1)
                except Exception:
                        self.brake(1)


if __name__ == "__main__":
        global bumperRef, distanceRef, angleRef
        bumperRef = []
        bumperRef.append(False)
        distanceRef = []
        distanceRef.append(0)
        angleRef = []
        angleRef.append(0)
        rospy.init_node('bumpGo', anonymous=True)
        rospy.Subscriber('sensorPacket', SensorPacket, recievePacket)
        bumpGo = BumpGo(bumperRef, distanceRef, angleRef)
        bumpGo.start()
        rospy.spin()
        bumpGo.go = False
        bumpGo.brake(1)

