from naoqi import ALProxy
import SectionVideo as sv
import TrackNao as tn
import CamlabTracking as ct
import CamLab as cl
import motion
import math
import time
import numpy as np

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

	# ESTABLECER LOS PARAMETROS
	lower_c = np.array((138,0,0))
	upper_c = np.array((180,223,167))

	# INICIAR LA CAMARA
	camlab = cl.Camera(url)
	camlab.move_camera()
	camlab.show=True
	camlab.save=True
	camlab.start()

	# INICIAR MOVIMIENTO
	Parar()
	motionProxy.moveInit()
	time.sleep(2)
	motionProxy.setWalkTargetVelocity(0.8,0.0,0,0.6)
	time.sleep(2)

	motionProxy.setWalkArmsEnabled(True, False)
	motionProxy.setWalkTargetVelocity(1.0,0.0,0,0.5)
	Bder(1)

	time.sleep(10)

	# FINALIZAR PROCESOS
	Deternerse()
	Sentar()
	if camlab.is_running():
		camlab.end_cam()

	# COMENZAR PROCESAMIENTO DE VIDEO Y ANALISIS
	section_v = sv.GetVideos(lower_c,upper_c)
	section_v.Cut()
	cheking=tn.GetData()
	cheking.Analyze()
	cheking2 = tn.GetData('Cut_video.avi')
	cheking2.Analyze()

if __name__ == "__main__":
	url = "http://192.168.0.100/image"
	robotIp = "148.226.221.158"
	robotPort = 9559
	main(robotIp,robotPort,url)