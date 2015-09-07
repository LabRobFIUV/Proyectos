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
        val=[0,0,0,0,0,0]
        val[0]=int(raw_input("Instruccion 1: "))

        if val[0]==0:
            break

        if val[0]==3 or val[0]==4:
            val[1]=int(raw_input("Instruccion 2: "))
            val[2]=int(raw_input("Instruccion 3: "))
            val[3]=int(raw_input("Instruccion 4: "))
            val[4]=int(raw_input("Instruccion 5: "))
            val[5]=int(raw_input("Instruccion 6: "))

        if val[0]==5:
            val='5'+raw_input("Frase: ")
            print val

        val=str(val)
        colaT.append(val)

    for i in colaT:
        try:
            talker(i)
        except rospy.ROSInterruptException:
            pass
