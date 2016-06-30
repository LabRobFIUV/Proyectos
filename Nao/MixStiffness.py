# CAMINAR COJEANDO
    motionProxy.stiffnessInterpolation("Body",1.0,1.0) # Segundo valor
    postureProxy.goToPosture("StandInit", 1.0)
    motionProxy.moveInit()
    motionProxy.move(0.05,0,0,[
    ["LeftStepHeight", 0.02],
    ["RightStepHeight", 0.005],
    ["RightTorsoWx", -7.0*almath.TO_RAD],
    ["TorsoWy", 5.0*almath.TO_RAD] ])
    
    time.sleep(5)
    motionProxy.stopMove()
    postureProxy.goToPosture("Crouch", 1.0)
    motionProxy.stiffnessInterpolation("Body",0,1.0)


# POSICIONES EN EL MUNDO
    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Example showing how to get a simplified robot position in world.
    useSensorValues = False
    result = motionProxy.getRobotPosition(useSensorValues)
    print "Robot Position", result

    # Example showing how to use this information to know the robot's diplacement.
    useSensorValues = False
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(useSensorValues))

    # Make the robot move
    motionProxy.moveTo(0.1, 0.0, 0.2)

    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(useSensorValues))

    # Compute robot's' displacement
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move:", robotMove

    # Go to rest position
    motionProxy.rest()



# CAMINAR Y MOVER VARIAS EXTREMIDADES
import sys
import time
import random
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP):
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 1.0)

    # Initialize the walk process.
    # Check the robot pose and take a right posture.
    # This is blocking called.
    motionProxy.moveInit()

    testTime = 10 # seconds
    t = 0
    dt = 0.2
    while (t<testTime):

        # WALK
        X         = .6
        Y         = 0
        Theta     = 0
        Frequency = .2
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

        # JERKY HEAD
        motionProxy.setAngles("HeadYaw", random.uniform(-1.0, 1.0), 0.1)
        motionProxy.setAngles("LShoulderRoll", random.uniform(-0.3, 1), 0.1)

        t = t + dt
        time.sleep(dt)

    # stop walk on the next double support
    motionProxy.stopMove()


if __name__ == "__main__":
    robotIp = "148.226.221.114"
    main(robotIp)






# CAMINAR Y TOMAR OBJETOS
from naoqi import ALProxy
import TrackNao as tn
import threading
import motion
import time
import math
import sys

def Bder():
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]

    ArmR=[80,-40,80,60,0]
    ArmR = [ x * motion.TO_RAD for x in ArmR]
    motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)

def Bizq():
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)

    ArmL = [90,80,-90,-50,-80]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)
    motionProxy.closeHand("LHand")

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)

def Parar():
    motionProxy.stiffnessInterpolation("Body",1,1.0)
    postureProxy.goToPosture("StandInit",1)

def Sentar():
    postureProxy.goToPosture("Crouch",1)
    motionProxy.stiffnessInterpolation("Body",0,1.0)

def Caminar():
    motionProxy.setWalkTargetVelocity(0.6,0,0,0.1)
    testTime = 10 # seconds
    t = 0
    dt = 0.2
    motionProxy.setWalkArmsEnabled(False, False)
    motionProxy.openHand("LHand")
    while (t<testTime):
        Bder()
        Bizq()
        t = t + dt
        time.sleep(dt)

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

    # INICIAR CAMARA
    cam = tn.Cam(url)
    cam.move_camera()
    cam.start()

    # PREPARARSE
    Parar()
    Caminar()
    time.sleep(8)

    # MOVIMIENTO
    
    der = threading.Thread(target=Bder)
    izq = threading.Thread(target=Bizq)
    der.start()
    izq.start()

    time.sleep(8)
    motionProxy.setWalkArmsEnabled(True,True)

    # TERMINAR TODO
    Deternerse()
    Sentar()
    cam.end_cam()

if __name__ == "__main__":
    url = "http://192.168.0.100/image"
    robotIp = "148.226.221.114"
    robotPort = 9559
    main(robotIp,robotPort,url)


# NO SE QUE ES ESTO
from naoqi import ALProxy
import TrackNao as tn
import threading
import motion
import time
import math
import sys

def Bder():
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]

    ArmR=[80,-40,80,60,0]
    ArmR = [ x * motion.TO_RAD for x in ArmR]
    motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)

def Bizq():
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)

    ArmL = [90,80,-90,-50,-80]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)
    motionProxy.closeHand("LHand")

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)

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

    # INICIAR CAMARA
    cam = tn.Cam(url)
    cam.move_camera()
    cam.start()

    # PREPARARSE
    Parar()
    Caminar()
    time.sleep(8)

    # MOVIMIENTO
    motionProxy.setWalkArmsEnabled(False, False)
    motionProxy.openHand("LHand")

    der = threading.Thread(target=Bder)
    izq = threading.Thread(target=Bizq)
    der.start()
    izq.start()

    time.sleep(8)
    motionProxy.setWalkArmsEnabled(True,True)

    # ESTE ES EL CHIDO QUE ESTABA COMENTADO ...
    # MOVIMIENTO
    motionProxy.setWalkArmsEnabled(False, False)
    Bder()
    Bizq()
    time.sleep(8)
    motionProxy.setWalkArmsEnabled(True,True)
    # HASTA AQUI

    # TERMINAR TODO
    Deternerse()
    Sentar()
    cam.end_cam()

if __name__ == "__main__":
    url = "http://192.168.0.100/image"
    robotIp = "148.226.221.114"
    robotPort = 9559
    main(robotIp,robotPort,url)



# TAREAS PARALELAS
def Bder():
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]

    ArmR=[80,-40,80,60,0]
    ArmR = [ x * motion.TO_RAD for x in ArmR]
    motionProxy.setAngles(RightArmjoints, ArmR,0.1)

def Bizq():
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    id_B1 = motionProxy.post.setAngles(LeftArmjoints, ArmL,0.1)
    motionProxy.wait(id_B1, 0)

    ArmL = [90,80,-90,-50,-80]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    id_B1 = motionProxy.post.setAngles(LeftArmjoints, ArmL,0.1)
    motionProxy.wait(id_B1, 0)
    #motionProxy.closeHand("LHand")

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    id_B1 = motionProxy.post.setAngles(LeftArmjoints, ArmL,0.1)
    motionProxy.wait(id_B1, 0)


# MOVER Y CAMINAR RARO
from naoqi import ALProxy
import TrackNao as tn
import threading
import motion
import time
import math
import sys

def MoverBrazos():
    time.sleep(3)
    motionProxy.setWalkArmsEnabled(False,False)
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]
    ArmR=[80,-40,80,60,0]
    ArmR = [ x * motion.TO_RAD for x in ArmR]
    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]

    t = 0
    while (t<3):
        motionProxy.setAngles(LeftArmjoints,ArmL, 0.1)
        motionProxy.setAngles(RightArmjoints,ArmR, 0.1)
        t = t + 0.2
        time.sleep(0.2)

    ArmL = [90,80,-90,-50,-80]
    ArmL = [ x * motion.TO_RAD for x in ArmL]

    t = 0
    while (t<3):
        motionProxy.setAngles(LeftArmjoints,ArmL, 0.1)
        t = t + 0.2
        time.sleep(0.2)

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    t = 0
    while (t<3):
        motionProxy.setAngles(LeftArmjoints,ArmL, 0.1)
        t = t + 0.2
        time.sleep(0.2)

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

    # INICIAR CAMARA
    cam = tn.Cam(url)
    cam.move_camera()
    cam.start()

    # PREPARARSE
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit",1)
    motionProxy.moveInit()

    # MOVIMIENTO
    motionProxy.move(0.03,0.0,0.0)
    MoverBrazos()
    time.sleep(8)
    motionProxy.setWalkArmsEnabled(True,True)

    # TERMINAR TODO
    motionProxy.stopMove()
    motionProxy.rest()
    cam.end_cam()

if __name__ == "__main__":
    url = "http://192.168.0.100/image"
    robotIp = "148.226.221.114"
    robotPort = 9559
    main(robotIp,robotPort,url)