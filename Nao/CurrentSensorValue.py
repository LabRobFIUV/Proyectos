from naoqi import ALProxy
import time

myMemProxy = ALProxy("ALMemory", "148.226.221.114", 9559)

while(1):
	sensor = myMemProxy.getData("Device/SubDeviceList/HeadYaw/ElectricCurrent/Sensor/Value")
	print sensor
	time.sleep(0.2)