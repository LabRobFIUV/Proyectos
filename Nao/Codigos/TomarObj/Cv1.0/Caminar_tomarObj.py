from naoqi import ALProxy
import SectionVideo as sv
import TrackNao as tn
import CamlabTracking as ct
import motion
import almath
import time

def Bder(val):
	RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]

	if(val==1):
		ArmR=[80,-40,80,60,0]
		ArmR = [ x * motion.TO_RAD for x in ArmR]
		motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)
	if(val==2):
		ArmR=[0,-40,0,30,90]
		ArmR = [ x * motion.TO_RAD for x in ArmR]
		motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)

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

	'''
	cam = sv.Cam(url)
	cam.move_camera()
	cam.start()
	Parar()
	motionProxy.moveInit()
	time.sleep(2)

	conf = [["MaxStepFrequency",0.1]]
	motionProxy.moveToward(0.5,0.0,0,conf)
	motionProxy.setWalkTargetVelocity(0.8,0.0,0,0.6)

	time.sleep(2)
	motionProxy.setWalkArmsEnabled(True, False)
	motionProxy.setWalkTargetVelocity(1.0,0.0,0,0.5)
	Bder(1)

	time.sleep(10)

	Deternerse()
	Sentar()
	cam.end_cam()

	cheking = tn.GetData()
	cheking.Analyze('videoT.avi')
	cheking2 = tn.GetData()
	cheking2.Analyze('video.avi')
	'''
	camlab = ct.Tobject(url)
	camlab.start()

if __name__ == "__main__":
	url = "http://192.168.0.100/image"
	robotIp = "148.226.221.158"
#	robotIp = "148.226.221.114"
	robotPort = 9559
	main(robotIp,robotPort,url)