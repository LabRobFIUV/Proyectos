#!/usr/bin/env python
from naoqi import ALProxy 
import rospy
import time
from std_msgs.msg import String

def talker(val):
    pub = rospy.Publisher('Sonar',String,queue_size=4)
    rospy.init_node('Sonar', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

def main(robotIp,robotPort):
    sonarProxy = ALProxy("ALSonar",robotIp,robotPort)
    sonarProxy.subscribe("Sensores")
    memoryProxy = ALProxy("ALMemory",robotIp,robotPort)
    while (1):
        left=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        right=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        val=[left,right]
        print val
        if left<0.3 and right<0.3:
            if left<right:
                talker("ObsL")
            else:
            	talker("ObsR")
            time.sleep(7)
            continue
        if left<0.3:
            talker("ObsL")
            time.sleep(7)
            continue
        if right<0.3:
            talker("ObsR")
            time.sleep(7)
            continue
    sonarProxy.unsubscribe("Sensores")

if __name__ == "__main__":
    robotIp = "148.226.221.114"
    robotPort = 9559
    main(robotIp,robotPort)
