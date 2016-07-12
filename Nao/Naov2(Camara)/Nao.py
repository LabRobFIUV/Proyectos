import rospy
from std_msgs.msg import Int32

from naoqi import ALProxy
import motion
import math
import time
import numpy as np

pub = rospy.Publisher('CM',Int32,queue_size=4)

def Bder(val):
	# Mueve el brazo derecho usando angulos en los joins
	RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]
	if(val==1):
		ArmR=[80,-40,80,60,0]
		ArmR = [ x * motion.TO_RAD for x in ArmR]
		motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)
	if(val==2):
		ArmR=[0,-40,0,30,90]
		ArmR = [ x * motion.TO_RAD for x in ArmR]
		motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)
	if(val==3):
		ArmR=[0,-40,0,40,90]
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

def Sequence():
	# Parar, Avanzar, Tomar objeto, Detenerse, Sentarse
	Parar()
	motionProxy.moveInit()
	time.sleep(2)
	motionProxy.setWalkTargetVelocity(0.8,0.0,0,0.6)
	time.sleep(2)
	motionProxy.setWalkArmsEnabled(True, False)
	Bder(1)
	motionProxy.setWalkTargetVelocity(1.0,0.0,0,0.5)
	time.sleep(5)
#	Bder(3)
	time.sleep(5)
	Deternerse()
	Sentar()
	time.sleep(2)
	pub.publish(2) # Publica que termino

def Opciones(data):
	c=data.data
	if c==11:
		Sequence() # Parar, Avanzar, Tomar objeto, Detenerse, Sentarse
	if c==12:
		Parar()
	if c==13:
		Sentar()

def main(robotIP,robotPort):
	global motionProxy
	global postureProxy
	# Instancia los metodos necesarios
	try:
		# Metodo para controlar el movimiento
		motionProxy = ALProxy("ALMotion", robotIP, robotPort)
	except Exception, e:
		print "Could not create proxy to ALMotion"
	try:
		# Metodo que contiene las posturas del robot, como sentarse o parado
		postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
	except Exception, e:
		print "Could not create proxy to ALRobotPosture"

	motionProxy.setWalkArmsEnabled(True, True)	# Mover brazos mientras camina
	# Si es levantado del suelo, detenerse
	motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

	rospy.init_node('Nao', anonymous=True)	# Inicia el nodo "Nao"
	rate = rospy.Rate(10)
	rospy.Subscriber("CN", Int32, Opciones)		# Suscribirse al nodo "CN"
	rate.sleep()
	rospy.spin()

if __name__ == "__main__":
	robotIp = "148.226.221.151"		# IP del robot
	robotPort = 9559				# Puerto por default
	main(robotIp,robotPort)