import cv2
import time
import math
import motion
import numpy as np
from naoqi import ALProxy

def Parar():
	motionProxy.stiffnessInterpolation("Body",1,1.0)
	postureProxy.goToPosture("StandInit",1)

def Sentar():
	postureProxy.goToPosture("Crouch",1)
	motionProxy.stiffnessInterpolation("Body",0,1.0)

def Caminar():
	motionProxy.setWalkTargetVelocity(0.8,0,0,0.8)

def Deternerse():
	motionProxy.setWalkTargetVelocity(0,0,0,0)

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

	result = motionProxy.getPosition("CameraTop", motion.FRAME_WORLD, True)
	print math.degrees(result[3])
	print math.degrees(result[4])
	print math.degrees(result[5])

	Parar()
	motionProxy.setWalkTargetVelocity(0.0,0,0.5,0.1)
#	Caminar()
	time.sleep(10)
	Deternerse()
	Sentar()

	print ""
	print math.degrees(result[3])
	print math.degrees(result[4])
	print math.degrees(result[5])

if __name__ == '__main__':
	robotIp = "148.226.221.158"
	robotPort = 9559
	main(robotIp,robotPort)