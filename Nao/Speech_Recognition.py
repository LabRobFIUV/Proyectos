#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys
import motion
import time
from naoqi import ALProxy

def talker(val):
    pub = rospy.Publisher('RVoz',String,queue_size=4)
    rospy.init_node('RVoz', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

def main(robotIP,robotPort):
    global asr
    global memory
    global band
    band=False

    try:
        asr = ALProxy("ALSpeechRecognition", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"
    try:
        memory = ALProxy("ALMemory",robotIp, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"

    asr.setLanguage("Spanish")
    vocabulary = ["Parate", "Sientate","Camina","Detente","Salir","A"]
    asr.setVocabulary(vocabulary,True)
    asr.setAudioExpression(False)

    asr.subscribe("ASR")
    memory.subscribeToEvent("SREvent","WordRecognized","WordRecognized")

    try:
        memory.removeData("WordRecognized")
        print "Se borro"
    except RuntimeError:
        print "No se borro"

    ant=[0,0]
    message=""

    while(1):
        print "WHILE"
        time.sleep(1.5)
        try:
            recolist=memory.getData("WordRecognized")
        except RuntimeError:
            print "Memoria Vacia"
            continue

        print recolist
        if ant[0]==recolist[0]:
            continue
        elif recolist[0]=="Salir":
            break
        else:
            ant=recolist
            message=recolist[0]
            talker(message)
        try:
            memory.removeData("WordRecognized")
            print "Se borro"
        except RuntimeError:
            print "No se borro"
            continue
    memory.removeData("WordRecognized")

    memory.unsubscribeToEvent("SREvent","WordRecognized")
    asr.unsubscribe("ASR")

if __name__ == "__main__":
    robotIp = "148.226.221.222"
    robotPort = 9559
    main(robotIp,robotPort)