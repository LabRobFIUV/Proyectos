import sys
import motion
import time
import math
from naoqi import ALProxy

'''
val=[90,0,0,0,-104]
val=[70,30,-100,-60,0]
val=[40,20,-100,-30,0]
val=[70,30,-100,-60,0]
'''

def callTec(c):
    print "callTec"
    if c[0]==1:
        print"Parar"
        Stiffness(motionProxy,1)
        Posture(postureProxy,"StandInit",1)
    if c[0]==2:
        print"Sentar"
        Posture(postureProxy,"Crouch",1)
        Stiffness(motionProxy,0)
    if c[0]==3:
        print"Caminar"
        Caminar(motionProxy,c[1]/10.0,c[2]/10.0,c[3]/10.0,c[4]/10.0)
        if c[5]!=0:
            time.sleep(c[5])
            Detenerse(motionProxy)
    if c[0]==4:
        print"Detener"
        Caminar(motionProxy,0,0,0,0)
    if c[0]==6:
        print "Brazo"
        motionProxy.setWalkArmsEnabled(False, True)
        motionProxy.openHand("LHand")

        Cuerpo(motionProxy,c[2:],c[1])
        '''
        val=[50,50,-120,-30,-10]
        Cuerpo(motionProxy,val,c[1])
        time.sleep(1)

        motionProxy.closeHand("LHand")

        val=[80,10,-100,-60,0]
        Cuerpo(motionProxy,val,c[1])
        #time.sleep(2)

        val=[70,30,-100,-60,0]
        #Cuerpo(motionProxy,val,c[1])
        motionProxy.setWalkArmsEnabled(True, True)
        '''

def Caminar(motionProxy,X,Y,Theta,Frequency):
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def Cuerpo(motionProxy,ArmL,Part):
    HeadJoins = ["HeadPitch", "HeadYaw"]
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]
    Pelvisjoints = ["RHipYawPitch", "LHipYawPitch"]
    LeftLegjoints = ["LHipPitch", "LHipRoll", "LKneePitch", "LAncklePitch","LAnckleRoll"]
    RightLegjoints = ["RHipPitch", "RHipRoll", "RKneePitch", "RAncklePitch","RAnckleRoll"]

    ArmL = [ x * motion.TO_RAD for x in ArmL]
    pFractionMaxSpeed = 0.2

    if Part==1:
        motionProxy.angleInterpolationWithSpeed(HeadJoins, ArmL, pFractionMaxSpeed)
    if Part==2:
        motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL, pFractionMaxSpeed)
    if Part==3:
        motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmL, pFractionMaxSpeed)
    if Part==4:
        motionProxy.angleInterpolationWithSpeed(Pelvisjoints, ArmL, pFractionMaxSpeed)
    if Part==5:
        motionProxy.angleInterpolationWithSpeed(LeftLegjoints, ArmL, pFractionMaxSpeed)
    if Part==6:
        motionProxy.angleInterpolationWithSpeed(LeftLegjoints, ArmL, pFractionMaxSpeed)

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
    global tts
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

    while(1):
        val=[0,0,0,0,0,0,0]
#        val[0]=int(raw_input("Instruccion: "))
        val[0]=2

        if val[0]==3:
            val[1]=6
            val[2]=0
            val[3]=0
            val[4]=1
            val[5]=0

        if val[0]==6:
            val[1]=3
            val[2]=0
            val[3]=-40 #int(raw_input("Angulo: "))
            val[4]=0
            val[5]=30
            val[6]=90
        callTec(val)

if __name__ == "__main__":
    robotIp = "148.226.221.158"
    robotPort = 9559
    main(robotIp,robotPort)
    val=[70,30,-100,-60,0]
    val=[50,50,-120,-30,-10]
    val=[80,10,-100,-60,0]