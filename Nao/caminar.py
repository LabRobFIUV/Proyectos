#!/usr/bin/env python
import rospy
from std_msgs.msg import String

import sys
import motion
import time
import math
from naoqi import ALProxy

def Obt_pos():
    chainName = "LArm"
    space     = motion.FRAME_TORSO
    useSensor = False
    current = motionProxy.getPosition(chainName, space, useSensor)
    return current

def Arrivar():
    '''
    a = Obt_pos()
    a[3]=math.degrees(a[3])
    a[4]=math.degrees(a[4])
    a[5]=math.degrees(a[5])
    ant=a[5]
    print a

    Caminar(motionProxy,0.0,0.0,0.4,0.2)

    while (ant+90)>a[5]:
        a = Obt_pos()
        a[3]=math.degrees(a[3])
        a[4]=math.degrees(a[4])
        a[5]=math.degrees(a[5])
        print a
    '''
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

def Posture(postureProxy,pose,velocity):
    postureProxy.goToPosture(pose, velocity)

def Stiffness(proxy,x):
    pNames = "Body"
    pStiffnessLists = x
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

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

    Stiffness(motionProxy,1)
    Posture(postureProxy,"StandInit",1)
    #listener()
    Arrivar()

    #postureProxy.goToPosture("Sit", 1)
    Stiffness(motionProxy,0)

if __name__ == "__main__":
    robotIp = "148.226.221.183"
    robotPort = 9559
    main(robotIp,robotPort)