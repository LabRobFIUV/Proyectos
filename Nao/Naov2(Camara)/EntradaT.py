import rospy
from std_msgs.msg import Int32

def main():
	pub = rospy.Publisher('CM',Int32,queue_size=4) 	# Se crear una variable para publicar informacion a otros nodos
	rospy.init_node('EntradaT', anonymous=True)		# Se inicia un nodo llamado "EntradaT"
	rate = rospy.Rate(10)							
	while True:
		val=int(raw_input("Instruccion: "))
		pub.publish(val)							# Publica lo que recibe
		rate.sleep()

if __name__ == '__main__':
	main()