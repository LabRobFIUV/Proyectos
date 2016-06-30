#!/usr/bin/python
import roslib; roslib.load_manifest('irobot_create_2_1')
import rospy

from geometry_msgs.msg import Twist
from irobot_create_2_1.msg import SensorPacket
from actionlib_msgs.msg import GoalID
from move_base_msgs.msg import MoveBaseActionGoal
import threading
#by carlos nuñez @carlos.19nh@gmail.com
global ban
ban=0

threads = list()

def callback3(data):
	global mbaGoal
	mbaGoal = data
def callback1(data):
	global ban

	if(data.bumpLeft or data.bumpRight):  #deteccion de bumper ya sea izquierdo, derecho o ambos 
		if(ban==0):			
			ban=1
			t = threading.Thread(target=diablo)#funcion retroceder 60 cm
			threads.append(t)
			t.start()
def diablo():
	global ban
	global goalId
	global mbaGoal
	
	goalId.stamp = rospy.Time.now()	 #cancela 
	goalId.id = ""			#la ruta actual
	pub2.publish(goalId)

        for i in range(60):
		twist.linear.x = -0.1
		twist.linear.y = 0.0
		twist.linear.z = 0.0
		twist.angular.x = 0.0
		twist.angular.y = 0.0
		twist.angular.z = 0.0
		pub.publish(twist)
		rospy.sleep(0.1)

	twist2 = Twist()
	pub.publish(twist2)
	
	pub3.publish(mbaGoal)  #enviar el goal antes cancelado
	
	ban=0
	
def listener():
    
    global twist
    global goalId
    global mbaGoal
    global pub
    global pub2
    global pub3
    

    mbaGoal = MoveBaseActionGoal()
    goalId = GoalID()
    twist = Twist()

    pub = rospy.Publisher('cmd_vel', Twist)
    pub2 = rospy.Publisher('/move_base/cancel', GoalID)
    pub3 = rospy.Publisher('/move_base/goal', MoveBaseActionGoal)

    rospy.init_node('read_sensor', anonymous=True)

    rospy.Subscriber("sensorPacket", SensorPacket, callback1)
    rospy.Subscriber("move_base/goal", MoveBaseActionGoal,callback3)
    rospy.spin()

if __name__ == '__main__':
    listener()
