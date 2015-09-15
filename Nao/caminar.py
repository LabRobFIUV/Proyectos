#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys
import motion
import time
import math
from naoqi import ALProxy

def Obt_pos():
    chainName = "Torso"
    space     = motion.FRAME_TORSO
    useSensor = False
    current = motionProxy.getPosition(chainName, space, useSensor)
    return current

def Arrivar():
    a = Obt_pos()
    ant=a[0]
    Caminar(motionProxy,0.8,0.0,0.0,0.2)
    print a
    while((ant[0]-0.1)<=a[0]):
        a=Obt_pos()
    print a
    Detenerse(motionProxy)

def Caminar(motionProxy,X,Y,Theta,Frequency):
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def Detenerse(motionProxy):
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency=0.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def main(robotIP,robotPort):
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

    proxy.stiffnessInterpolation("Body",1,1.0)

    postureProxy.goToPosture("StandInit",1)
    Arrivar()

    proxy.stiffnessInterpolation("Body",0,1.0)

if __name__ == "__main__":
    robotIp = "148.226.221.183"
    robotPort = 9559
    main(robotIp,robotPort)