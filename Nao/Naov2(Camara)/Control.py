#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
pub = rospy.Publisher('CC',Int32,queue_size=4)
pub2 = rospy.Publisher('CN',Int32,queue_size=4)

def ManualC(data):
	c=data.data
	# Dependiendo lo que reciba, publica a cierto nodo
	if c<=10:
		pub.publish(c)	# publica a CC
	if c>10 and c<=20:
		pub2.publish(c)	# publica a CN

def main():
	rospy.init_node('Control', anonymous=True)	# Inicia un nodo llamado "Control"
	rate = rospy.Rate(10)						
	rospy.Subscriber("CM", Int32, ManualC)		# Se suscribe al nodo CM
	rate.sleep()
	rospy.spin()

if __name__ == '__main__':
	main()