#!/usr/bin/env python
# Viveros Aguilar Jesus Martin
import rospy
import std_msgs.msg as std

def talker(val):
    pub = rospy.Publisher('prueba',std.String,queue_size=4)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

if __name__ == '__main__':
    colaT=[]
    while(1):
        val=[0,0,0,0,0,0,0]
        val[0]=int(raw_input("Instruccion 1: "))

        if val[0]==3:
            print "escala 1 es 10"
            val[1]=int(raw_input("X: "))
            val[2]=int(raw_input("Y: "))
            val[3]=int(raw_input("Theta: "))
            val[4]=int(raw_input("Frequency: "))
            val[5]=int(raw_input("Time sleep: "))

        if val[0]==4:
            val[1]=int(raw_input("Parte del cuerpo: "))
            val[2]=int(raw_input("Angulo 1: "))
            val[3]=int(raw_input("Angulo 2: "))
            val[4]=int(raw_input("Angulo 3: "))
            val[5]=int(raw_input("Angulo 4: "))
            val[6]=int(raw_input("Angulo 5: "))

        if val[0]==5:
            val='5'+raw_input("Frase: ")
            print val

        if val[0]==7:
            val[1]=int(raw_input("Numero de pose"))

        if val[0]==0:
            break;

        val=str(val)
        colaT.append(val)

    for i in colaT:
        try:
            talker(i)
        except rospy.ROSInterruptException:
            pass
